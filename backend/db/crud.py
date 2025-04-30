from .supabase_client import supabase
from datetime import datetime

def create_conversation(title: str, date: str):
    response = supabase.table("conversations").insert({
        "title": title,
        "date": date
    }).execute()

    if response.data:
        return response.data[0]  # Prend le premier élément de la liste
    else:
        raise Exception("Erreur lors de la création de la conversation.")

def get_conversations():
    response = supabase.table("conversations").select("*").execute()
    return response.data

def create_message(conversation_id: int, message: str, response_text: str, timestamp: str):
    response = supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "message": message,
        "response": response_text,
        "timestamp": timestamp
    }).execute()

    if response.data:
        return response.data[0]
    else:
        raise Exception("Erreur lors de la création du message.")
