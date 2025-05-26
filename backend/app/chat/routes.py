
#backend/app/chat/routes.py


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.chat import service
from app import schemas

router = APIRouter(prefix="/chat", tags=["chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/conversation", response_model=schemas.ConversationOut)
def create_conv(conv: schemas.ConversationCreate, user_id: int, db: Session = Depends(get_db)):
    return service.create_conversation(db, user_id=user_id, title=conv.title)

@router.get("/conversations/{user_id}", response_model=list[schemas.ConversationOut])
def get_convs(user_id: int, db: Session = Depends(get_db)):
    return service.get_conversations(db, user_id=user_id)

@router.post("/message", response_model=schemas.MessageOut)
def post_msg(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    return service.add_message(db, msg.conversation_id, msg.sender, msg.content)

@router.get("/messages/{conversation_id}", response_model=list[schemas.MessageOut])
def get_msgs(conversation_id: int, db: Session = Depends(get_db)):
    return service.get_messages(db, conversation_id)
