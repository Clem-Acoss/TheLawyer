
#chat.py



from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import crud
from datetime import datetime
from db.crud import add_message
router = APIRouter()

# Pydantic model pour la nouvelle conversation
class NewConversation(BaseModel):
    user_id: int
    title: str
    message: str

class MessageRequest(BaseModel):
    user_id: int
    title: str
    message: str
    date: datetime  
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

@router.get("/messages/{user_id}/{conversation_title}")
async def get_messages_for_conversation(conversation_title: str):
    """
    Récupère les messages d'une conversation spécifique.
    """
    messages = crud.get_messages_by_conversation_title(conversation_title)
    if not messages:
        raise HTTPException(status_code=404, detail="Aucun message trouvé pour cette conversation")
    return messages

@router.delete("/conversations/{title}")
async def delete_conversation(title: str):
    success = crud.delete_conversation_by_title(title)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")
    return {"message": f"Conversation '{title}' supprimée avec succès."}

@router.post("/send-message")
async def send_message(request: MessageRequest):
    # Récupérer le message et la réponse
    user_id=request.user_id
    title = request.title
    message = request.message
    date = request.date  # Récupère la date passée dans la requête
   
    # Ajouter le message au fichier CSV
    try:
        add_message(user_id,title,message,date)
        return {"message": "Message ajouté avec succès"}
    except Exception as e:
        print(f"Erreur lors de l'ajout du message : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du message")