from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from .chat_basic_ai_inference import generate_chat_stream
import json
import pydantic
import fastapi

app = FastAPI()


class Message(pydantic.BaseModel):
    content: str
    role: str = "user"


class ChatRequest(pydantic.BaseModel):
    messages: list[Message]


app.mount("/static", StaticFiles(directory="api/static"), name="static")
templates = Jinja2Templates(directory="api/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.post("/chat/stream")
async def chat_stream_handler(chat_request: ChatRequest) -> fastapi.responses.StreamingResponse:

    async def response_stream():
        messages = [{"role": message.role, "content": message.content} for message in chat_request.messages]
        chat_coroutine = generate_chat_stream(messages)
        for event in chat_coroutine:
            if event.choices:
                print(f"event = {event}")
                first_choice = event.choices[0]
                yield json.dumps({"delta": {"content": first_choice.delta.content, "role": first_choice.delta.role}}, ensure_ascii=False) + "\n"

    return fastapi.responses.StreamingResponse(response_stream())

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

