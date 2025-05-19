from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from db import crud
from services.chat_service import (
    generate_response_and_save,       # RAG
    generate_llm_response_and_save,  # LLM seul
)


router = APIRouter()

class NewConversation(BaseModel):
    user_id: int
    title: str
    message: str

class MessageRequest(BaseModel):
    user_id: int
    title: str
    message: str

@router.post("/conversations")
async def create_conversation(conv: NewConversation):
    data = crud.add_conversation(
        user_id=conv.user_id,
        title=conv.title,
        message=conv.message,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return {"message": "Conversation créée", "conversation": data}

@router.get("/conversations/{user_id}")
async def get_conversations(user_id: int):
    convs = crud.get_conversations_by_user(user_id)
    if not convs:
        raise HTTPException(404, "Aucune conversation trouvée")
    return convs

@router.get("/messages/{user_id}/{conversation_title}")
async def get_messages(user_id: int, conversation_title: str):
    msgs = crud.get_messages_by_conversation_title(user_id, conversation_title)
    if not msgs:
        raise HTTPException(404, "Aucun message pour cette conversation")
    return msgs

@router.delete("/conversations/{title}")
async def delete_conversation(title: str):
    if not crud.delete_conversation_by_title(title):
        raise HTTPException(404, "Conversation non trouvée")
    return {"message": f"Conversation '{title}' supprimée."}

@router.post("/send-message")
async def send_message(req: MessageRequest):
    try:
        print("→ Requête send-message:", req.dict())
        answer = generate_response_and_save(req.user_id, req.title, req.message)
        return {"answer": answer}
    except Exception as e:
        # imprime la stack complète dans la console
        import traceback
        traceback.print_exc()
        # renvoie aussi le message d’erreur dans le body
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")


@router.post("/send-message-llm")
async def send_message_llm(req: MessageRequest):
    """
    Route qui génère une réponse via LLM seul (pas de RAG).
    """
    try:
        answer = generate_llm_response_and_save(req.user_id, req.title, req.message)
        return {"answer": answer}
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(500, detail=str(e))