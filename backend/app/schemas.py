
#backend/app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ConversationCreate(BaseModel):
    title: str

class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    content: str

class MessageOut(BaseModel):
    id: int
    sender: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
