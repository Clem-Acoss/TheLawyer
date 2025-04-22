from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import uuid
import shutil
import requests

app = FastAPI()

# Autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#API_TOKEN
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# URL de l'API Hugging Face pour le modèle GPT-2
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# Stockage fictif des conversations (à remplacer par une base réelle)
conversations = [
    {"id": "1", "title": "Question sur le droit du travail", "date": "18 Avr. 2025"},
    {"id": "2", "title": "Conseil juridique", "date": "17 Avr. 2025"},
]

@app.get("/conversations")
def get_conversations():
    return conversations

@app.post("/chat")
async def chat(
    message: str = Form(...),
    files: List[UploadFile] = File(default=[]),
):
    # Simuler le traitement IA (à remplacer par appel à Hugging Face)
    print("Message reçu:", message)

    for file in files:
        contents = await file.read()
        print(f"Fichier reçu: {file.filename} ({len(contents)} octets)")
        # Sauvegarde locale si nécessaire
        # with open(f"uploads/{file.filename}", "wb") as f:
        #     f.write(contents)

    # Appel à l'API Hugging Face pour générer une réponse avec le modèle GPT-2
    response = requests.post(
        MODEL_URL, 
        headers=HEADERS, 
        json={"inputs": message},
        verify = False
    )
    print("Réponse brute du modèle :", response.text) 
    # Récupérer la réponse du modèle
    if response.status_code == 200:
        response_data = response.json()
        generated_text = response_data[0]['generated_text']
    else:
        generated_text = "Désolé, il y a eu une erreur lors de la génération de la réponse."

    # Retourner la réponse générée
    return {"response": generated_text}

# Endpoint test simple
@app.get("/")
def root():
    return {"message": "API backend IA juridique opérationnelle."}
