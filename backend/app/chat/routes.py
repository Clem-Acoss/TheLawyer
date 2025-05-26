
#backend/app/chat/routes.py


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.chat import service
from app import schemas, models
from app.auth.deps import get_db, get_current_user  # ✅ import des dépendances
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/conversation", response_model=schemas.ConversationOut)
def create_conv(
    conv: schemas.ConversationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ✅ récupération depuis le token
):
    return service.create_conversation(db, user_id=current_user.id, title=conv.title)

@router.get("/conversations", response_model=List[schemas.ConversationOut])
def get_convs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ✅ on ne passe plus le user_id dans l'URL
):
    return service.get_conversations(db, user_id=current_user.id)

@router.post("/send-message", response_model=schemas.MessageOut)
def post_msg(
    msg: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return service.add_message(db, msg.conversation_id, msg.sender, msg.content, msg.is_ai)

@router.get("/messages/{conversation_id}", response_model=List[schemas.MessageOut])
def get_msgs(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ✅ protection des messages
):
    # Optionnel : vérifier que current_user est bien propriétaire de la conversation
    return service.get_messages(db, conversation_id)

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")

    db.delete(conv)
    db.commit()
    return {"detail": "Conversation supprimée avec succès"}