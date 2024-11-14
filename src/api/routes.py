import json

import fastapi
import pydantic
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .shared import globals

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="api/templates")


class Message(pydantic.BaseModel):
    content: str
    role: str = "user"


class ChatRequest(pydantic.BaseModel):
    messages: list[Message]


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat/stream")
async def chat_stream_handler(
    chat_request: ChatRequest,
) -> fastapi.responses.StreamingResponse:
    chat_client = globals["chat"]
    if chat_client is None:
        raise Exception("Chat client not initialized")

    async def response_stream():
        messages = [
            {"role": message.role, "content": message.content}
            for message in chat_request.messages
        ]
        SYSTEM_PROMPT = "You are a helpful assistant."
        model_deployment_name = "gpt-4o-mini"
        system_message = [{"role": "system", "content": SYSTEM_PROMPT}]
        chat_coroutine = await chat_client.complete(
            model=model_deployment_name, messages=system_message + messages, stream=True
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

    return fastapi.responses.StreamingResponse(response_stream())
