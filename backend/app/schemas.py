"""
Fichier : schemas.py
--------------------

Définition des schémas Pydantic utilisés pour la validation et la sérialisation des données
dans les échanges API.

Schémas principaux :
- UserCreate / UserOut : création et sortie d’un utilisateur.
- Token : données du jeton d’accès JWT.
- ConversationCreate / ConversationOut : création et sortie d’une conversation.
- MessageCreate / MessageOut : création et sortie d’un message.
- MessageRequest : structure pour l’envoi de message via l’API.
- QuestionRequest : structure pour poser une question avec option conversation associée.

Caractéristiques techniques :
- Utilisation de Pydantic pour validation automatique et gestion ORM mode.
- Typage précis avec EmailStr, datetime, bool, Optional.
- Séparation claire entre modèles d’entrée (Create, Request) et de sortie (Out).
- Gestion des champs optionnels et valeurs par défaut.

Remarques :
- Ces schémas facilitent l’intégration et la documentation automatique (OpenAPI).
- Adaptés au backend FastAPI pour garantir cohérence des données échangées.
"""


from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from pydantic import ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class ConversationCreate(BaseModel):
    title: str

class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    content: str
    is_ai: bool = False  

class MessageOut(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime
    is_ai: bool

    model_config = ConfigDict(from_attributes=True)
        
class MessageRequest(BaseModel):
    conversation_id: int
    sender: str
    content: str

class QuestionRequest(BaseModel):
    question: str
    conversation_id: Optional[int] = None


class PasswordResetRequest(BaseModel):

    email: EmailStr

class PasswordResetTokenPayload(BaseModel):
    sub: str  

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str