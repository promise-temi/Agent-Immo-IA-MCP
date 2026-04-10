# Imports des librairies nécessaires
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from langchain_core.messages import AIMessage
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware




import sys
from pathlib import Path
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root_path))

from Agent.agent_servive import agent_run

# création de l'application FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Route de base pour vérifier l'application
@app.get("/")
def home():
    return { "message": "Bienvenue dans l'API de l'agent immobilier!"}

@app.get("/conversation", response_class=HTMLResponse)
def conversation(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.post("/agent")
async def run_agent_endpoint(request: Request):
    data = await request.json()
    user_prompt = data.get("message")

    if not user_prompt:
        return {"error": "Aucun message fourni"}

    print("Message reçu :", user_prompt)

    response = agent_run(user_prompt)

    messages = response.get("messages") or response.get("input") or []
    answer = ""

    for message in reversed(messages):
        if isinstance(message, AIMessage):
            answer = message.content
            break

    return {"response": answer}