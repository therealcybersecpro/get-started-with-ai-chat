from fastapi import FastAPI, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .chat_basic_ai_inference import generate_chat, generate_chat_stream

app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get('/')
def read_form():
    return 'hello world'


@app.get("/chat")
async def form_post(request: Request):
    result = "Enter your prompt"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/chat")
async def form_post(request: Request, query: str = Form(...)):
    result = generate_chat(query)
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.get("/chat/stream")
async def form_post(request: Request):
    result = "Enter your prompt"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/chat/stream")
async def form_post(request: Request, query: str = Form(...)):
    result = generate_chat_stream(query)
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})