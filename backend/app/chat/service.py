
#backend/app/chat/service.py




from sqlalchemy.orm import Session
from app import models

def create_conversation(db: Session, user_id: int, title: str):
    conv = models.Conversation(title=title, user_id=user_id)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversations(db: Session, user_id: int):
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).all()

def add_message(db: Session, conversation_id: int, sender: str, content: str):
    msg = models.Message(conversation_id=conversation_id, sender=sender, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, conversation_id: int):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
