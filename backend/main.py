#main.py



from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import os
from dotenv import load_dotenv
from db import crud
from services.chat_service import generate_response
from routes import chat, auth

# Initialisation de FastAPI
app = FastAPI()

# Inclure le router d'authentification
app.include_router(auth.router)
app.include_router(chat.router)
# Autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # L'URL de ton frontend
    allow_credentials=True,
    allow_methods=["*"],  # Toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Toutes les entêtes HTTP
)

# Charger les variables d'environnement
load_dotenv()
API_TOKEN = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# URL de l'API Hugging Face pour le modèle GPT-2
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# Endpoint pour récupérer toutes les conversations
@app.get("/conversations")
def get_conversations():
    return crud.get_conversations()  # Utiliser la méthode get_conversations du crud

# Endpoint pour récupérer les conversations d'un utilisateur spécifique



# Endpoint pour envoyer un message au chatbot et recevoir une réponse
@app.post("/chat")
async def chat(
    message: str = Form(...),
    files: List[UploadFile] = File(default=[]),
):
    # Générer la réponse du chatbot
    generated_text = generate_response(message)

    # Créer une nouvelle conversation et ajouter un message
    conversation = crud.add_conversation(
        title="Conseil juridique",
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    conversation_id = conversation["id"]

    # Ajouter les messages (utilisateur et réponse)
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
