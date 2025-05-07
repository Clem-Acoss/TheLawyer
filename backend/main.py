from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import uuid
import shutil
import requests
from dotenv import load_dotenv
from db import crud
from services.chat_service import generate_response
import os 
import httpx
import certifi
from routes import chat, auth 

os.environ["PYTHONHTTPSVERIFY"] = "0"
cert_path = r"C:\Users\ac75009559\AppData\Local\Programs\Python\Python313\Lib\site-packages\certifi\cacert.pem"
app = FastAPI()
app.include_router(auth.router)
# Autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#API_TOKEN
load_dotenv()
API_TOKEN= os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}
#Info pour supabase (Api key +url )
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# URL de l'API Hugging Face pour le modèle GPT-2
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# Stockage fictif des conversations (à remplacer par une base réelle)
conversations = [
    {"id": "1", "title": "Question sur le droit du travail", "date": "18 Avr. 2025"},
    {"id": "2", "title": "Conseil juridique", "date": "17 Avr. 2025"},
    {"id": "3", "title": "Conseil juridique", "date": "17 Avr. 2025"},
]

@app.get("/conversations")
def get_conversations():
    return conversations

@app.post("/chat")
async def chat(
    message: str = Form(...),
    files: List[UploadFile] = File(default=[]),
):
    generated_text = generate_response(message)

    conversation = crud.create_conversation(
        title="Conseil juridique",
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    conversation_id = conversation["id"]

    crud.create_message(
        conversation_id=conversation_id,
        message=message,
        response_text=generated_text,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return {"response": generated_text}


# Endpoint test simple
@app.get("/")
def root():
    return {"message": "API backend IA juridique opérationnelle."}
