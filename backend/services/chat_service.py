# chat_service.py 


import requests
from datetime import datetime
from db import crud
from dotenv import load_dotenv
import os 
from services.faiss_service import ask_question_pipeline

load_dotenv()
API_TOKEN= os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}
#Info pour supabase (Api key +url )
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# URL de l'API Hugging Face pour le modèle GPT-2
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}  # Tu peux passer l'API_TOKEN en paramètre si nécessaire

from services.faiss_service import ask_question_pipeline

def generate_response_and_save(user_id: int, title: str, message: str) -> str:
    """
    Appelle ask_question_pipeline(user_id, title, question) qui :
      - recherche via FAISS
      - génère la réponse avec Ollama
      - enregistre question + réponse dans le CSV
    Retourne uniquement la réponse texte.
    """
    result = ask_question_pipeline(user_id, title, message)
    return result["answer"]

def save_conversation_and_message(user_id: int, message: str, generated_text: str) -> dict:
    """
    Sauvegarder la conversation et le message dans le CSV.
    """
    # Créer une nouvelle conversation
    conversation = crud.add_conversation(user_id=user_id, title="Conseil juridique", message=message, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Sauvegarder le message et la réponse dans CSV
    crud.add_message(conversation_id=conversation["id"], message=message, response=generated_text, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return conversation 