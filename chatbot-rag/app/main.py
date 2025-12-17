import os
import threading
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import DOCS_PATH
from app.schemas import Question, Prospect
from app.rag import ask_question

from app.services.intent import wants_human_contact
from app.services.mailer import send_email
from app.services.watcher import start_watcher
from app.prospects_db import init_db, save_prospect


app = FastAPI(title="Chat RAG")

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # en prod: dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


# ---------------- CHAT ----------------

@app.post("/chat")
def chat(q: Question):
    if wants_human_contact(q.question):
        return {
            "answer": (
                "Perfecto 🙂\n\n"
                "Si deseas que alguien de nuestro equipo te contacte, "
                "por favor completa el formulario que aparece a continuación."
            ),
            "show_form": True
        }

    return {"answer": ask_question(q.question)}


# ---------------- DOCUMENTS ----------------

@app.get("/documents")
def list_documents():
    return {"documents": os.listdir(DOCS_PATH)}


# ---------------- PROSPECTS ----------------

@app.post("/prospect")
def create_prospect(p: Prospect, background_tasks: BackgroundTasks):
    save_prospect(p.name, p.email, p.message)

    background_tasks.add_task(
        send_email,
        p.email,
        "Hemos recibido tu solicitud",
        f"Hola {p.name},\n\n"
        "Gracias por tu interés. "
        "Pronto alguien de nuestro equipo se pondrá en contacto contigo.\n\n"
        "Saludos."
    )

    return {"status": "ok"}


# ---------------- STARTUP ----------------

@app.on_event("startup")
def startup_event():
    init_db()
    threading.Thread(
        target=start_watcher,
        daemon=True
    ).start()
