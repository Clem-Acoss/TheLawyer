# chat_service.py 


import requests
from datetime import datetime
from db import crud
from dotenv import load_dotenv
import os 

load_dotenv()
API_TOKEN= os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}
#Info pour supabase (Api key +url )
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# URL de l'API Hugging Face pour le modèle GPT-2
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}  # Tu peux passer l'API_TOKEN en paramètre si nécessaire

def generate_response(message: str) -> str:
    """
    Appel à l'API Hugging Face pour générer une réponse basée sur le message.
    """
    # Appel à l'API Hugging Face pour générer une réponse avec le modèle GPT-2
    response = requests.post(
        MODEL_URL,
        headers=HEADERS,
        json={"inputs": message},
        verify=False
    )

    if response.status_code == 200:
        response_data = response.json()
        return response_data[0]['generated_text']
    else:
        return "Désolé, il y a eu une erreur lors de la génération de la réponse."

def save_conversation_and_message(user_id: int, message: str, generated_text: str) -> dict:
    """
    Sauvegarder la conversation et le message dans le CSV.
    """
    # Créer une nouvelle conversation
    conversation = crud.add_conversation(user_id=user_id, title="Conseil juridique", message=message, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Sauvegarder le message et la réponse dans CSV
    crud.add_message(conversation_id=conversation["id"], message=message, response=generated_text, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return conversation 