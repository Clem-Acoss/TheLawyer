from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import crud
from datetime import datetime

router = APIRouter()

# Pydantic model pour la nouvelle conversation
class NewConversation(BaseModel):
    user_id: int
    title: str
    message: str

@router.post("/conversations")
async def create_conversation(conversation: NewConversation):
    """
    Créer une nouvelle conversation avec un titre.
    """
    try:
        # Appel à la méthode du CRUD pour enregistrer la conversation dans la base de données
        conversation_data = crud.add_conversation(
            user_id=conversation.user_id,
            title=conversation.title,
            message=conversation.message,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return {"message": "Conversation créée", "conversation": conversation_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la conversation")


@router.get("/conversations/{user_id}")
async def get_conversations(user_id: int):
    # Récupère les conversations pour l'utilisateur donné
    conversations = crud.get_conversations_by_user(user_id)
    if not conversations:
        raise HTTPException(status_code=404, detail="Aucune conversation trouvée")
    return conversations
