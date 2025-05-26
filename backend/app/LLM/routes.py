from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
from app.schemas import MessageRequest, MessageOut
from app.auth.deps import get_db
from app import crud, models
from app.auth.deps import get_current_user
from app.schemas import MessageCreate
router = APIRouter()

@router.post("/chat/send-message-llm", response_model=MessageOut)
def send_message_llm(
    request: MessageRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Crée un objet MessageCreate pour le message utilisateur
    user_message_data = MessageCreate(
        conversation_id=request.conversation_id,
        sender=request.sender,
        content=request.content,
        is_ai=False
    )
    user_message = crud.create_message(db=db, message_data=user_message_data)

    # Appel au modèle local
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": request.content,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur de connexion au modèle local : {e}")

    result = response.json()
    ai_response = result.get("response", "[Réponse vide]")

    # Crée un objet MessageCreate pour la réponse IA
    ai_message_data = MessageCreate(
        conversation_id=request.conversation_id,
        sender="assistant",
        content=ai_response,
        is_ai=True
    )
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    return ai_message
