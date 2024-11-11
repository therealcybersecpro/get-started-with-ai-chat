from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from .chat_basic_ai_inference import generate_chat, generate_chat_stream
import json
from fastapi.responses import StreamingResponse
import pydantic
from pydantic import BaseModel
import fastapi
#from chat_basic_ai_inference import generate_chat, generate_chat_stream


#app = fastapi.APIRouter()
app = FastAPI()


class Message(pydantic.BaseModel):
    content: str
    role: str = "user"


class ChatRequest(pydantic.BaseModel):
    messages: list[Message]


SYSTEM_PROMPT = """You are a helpful assistant."""


app.mount("/static", StaticFiles(directory="api/static"), name="static")
templates = Jinja2Templates(directory="api/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.post("/chat/stream")
async def chat_stream_handler(chat_request: ChatRequest) -> fastapi.responses.StreamingResponse:
    #messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_request.messages
    # Azure Open AI takes the deployment name as the model name
    #model = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "chatgpt")

    async def response_stream():
        '''chat_coroutine = clients["openai"].chat.completions.create(
            model=model,
            messages=messages,
            stream=True,       
        )'''
        chat_coroutine = generate_chat_stream(chat_request.messages)
        async for event in await chat_coroutine:
            if event.choices:
                first_choice = event.model_dump()["choices"][0]
                yield json.dumps({"delta": first_choice["delta"]}, ensure_ascii=False) + "\n"

    return fastapi.responses.StreamingResponse(response_stream())

'''@app.post("/chat/stream")
async def chat_handler(request: Request, message: str = Form(...)):
    request_messages = (await request.json)["messages"]
    async def response_stream():
        # This sends all messages, so API request may exceed token limits
        chat_coroutine = generate_chat_stream(request_messages)
        try:
            async for event in await chat_coroutine:
                event_dict = event.model_dump()
                if event_dict["choices"]:
                    yield json.dumps(event_dict["choices"][0], ensure_ascii=False) + "\n"
        except Exception as e:
            #current_app.logger.error(e)
            yield json.dumps({"error": str(e)}, ensure_ascii=False) + "\n"

    return templates.TemplateResponse('index.html', context={'request': request, 'result': response_stream()})

'''
# Generate Stream
async def stream_processor(response):
    async for chunk in response:
        if len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content




# Prompt
class Prompt(BaseModel):
    input: str

# API Endpoint

@app.post("/stream")
async def stream(request: Request, message: str = Form(...)):
    '''azure_open_ai_response = await client.chat.completions.create(
        model=deployment,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt.input}],
        stream=True
    )'''

    azure_open_ai_response = await generate_chat(message)

    return StreamingResponse(stream_processor(azure_open_ai_response), media_type="text/event-stream")


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

