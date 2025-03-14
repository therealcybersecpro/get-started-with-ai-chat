# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.
# See LICENSE file in the project root for full license information.
import json
import logging
import os

import fastapi
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from azure.ai.inference.prompts import PromptTemplate
from azure.ai.inference import ChatCompletionsClient

from .util import get_logger, ChatRequest
from .search_index_manager import SearchIndexManager
from azure.core.exceptions import HttpResponseError


logger = get_logger(
    name="azureaiapp_routes",
    log_level=logging.INFO,
    log_file_name=os.getenv("APP_LOG_FILE"),
    log_to_console=True
)

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="api/templates")


# Accessors to get app state
def get_chat_client(request: Request) -> ChatCompletionsClient:
    return request.app.state.chat


def get_chat_model(request: Request) -> str:
    return request.app.state.chat_model


def get_search_index_namager(request: Request) -> SearchIndexManager:
    return request.app.state.search_index_manager


@router.get("/", response_class=HTMLResponse)
async def index_name(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat/stream")
async def chat_stream_handler(
    chat_request: ChatRequest,
    chat_client: ChatCompletionsClient = Depends(get_chat_client),
    model_deployment_name: str = Depends(get_chat_model),
    search_index_manager: SearchIndexManager = Depends(get_search_index_namager)
) -> fastapi.responses.StreamingResponse:
    if chat_client is None:
        raise Exception("Chat client not initialized")

    async def response_stream():
        messages = [{"role": message.role, "content": message.content} for message in chat_request.messages]

        prompt_messages = PromptTemplate.from_string('You are a helpful assistant').create_messages()
        # Use RAG model, only if we were provided index and we have found a context there.
        if search_index_manager is not None:
            context = await search_index_manager.search(chat_request)
            if context:
                prompt_messages = PromptTemplate.from_string(
                    'You are a helpful assistant that answers some questions '
                    'with the help of some context data.\n\nHere is '
                    'the context data:\n\n{{context}}').create_messages(data=dict(context=context))
                logger.info(f"{prompt_messages=}")
            else:
                logger.info("Unable to find the relevant information in the index for the request.")
        try:
            chat_coroutine = await chat_client.complete(
                model=model_deployment_name, messages=prompt_messages + messages, stream=True
            )
            async for event in chat_coroutine:
                if event.choices:
                    first_choice = event.choices[0]
                    yield (
                        json.dumps(
                            {
                                "delta": {
                                    "content": first_choice.delta.content,
                                    "role": first_choice.delta.role,
                                }
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
        except BaseException as e:
            error_processed = False
            response = "<div class=\"error\">Error: {}</div>"
            try:
                if '(content_filter)' in e.args[0]:
                    rai_dict = e.response.json()['error']['innererror']['content_filter_result']
                    errors = []
                    for k, v in rai_dict.items():
                        if v['filtered']:
                            if 'severity' in v:
                                errors.append(f"{k}, severity: {v['severity']}")
                            else:
                                errors.append(k)
                    error_text = f"We have found the next safety issues in the response: {', '.join(errors)}"
                    logger.error(error_text)
                    response = response.format(error_text)
                    error_processed = True
            except BaseException:
                pass
            if not error_processed:
                error_text = str(e)
                logger.error(error_text)
                response = response.format(error_text)
            yield (
                json.dumps(
                    {
                        "delta": {
                            "content": response,
                            "role": "agent",
                        }
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    return fastapi.responses.StreamingResponse(response_stream())
