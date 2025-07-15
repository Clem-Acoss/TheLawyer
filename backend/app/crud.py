
"""
Fichier : crud.py
------------------

Ce module gère les opérations CRUD (Create, Read, Update, Delete) sur les entités principales de l’application.

Il permet d’interagir avec la base de données via SQLAlchemy et couvre les objets suivants :
- Utilisateurs (`User`)
- Conversations (`Conversation`)
- Messages (`Message`)

Fonctionnalités principales :
- Gestion des utilisateurs : création, récupération par email ou ID, authentification
- Gestion des conversations : création, récupération par utilisateur, suppression sécurisée par utilisateur
- Gestion des messages : création et récupération par conversation

Dépendances :
- `Session` de SQLAlchemy pour la gestion des transactions
- Fonctions de hachage et vérification de mot de passe pour la sécurité utilisateur
- Schémas Pydantic pour la validation des données en entrée

Remarques :
- Chaque fonction engage une transaction, commite et rafraîchit l’objet pour retourner l’état à jour
- Les suppressions sont sécurisées par contrôle de l’utilisateur propriétaire
- Les fonctions retournent des instances ORM ou des listes d’objets, ou `None` si aucun résultat

Ce module est utilisé par les couches API et services pour accéder aux données métiers.
"""




from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import User, Conversation, Message
from app.schemas import UserCreate, ConversationCreate, MessageCreate
from app.auth.utils import verify_password, hash_password
from app import models

# ---------- USER ----------

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


# ---------- CONVERSATION ----------

def create_conversation(db: Session, conversation_data: ConversationCreate, user_id: int) -> Conversation:
    conversation = Conversation(title=conversation_data.title, user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversations_by_user(db: Session, user_id: int) -> List[Conversation]:
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).all()


def get_conversation_by_id(db: Session, conversation_id: int) -> Optional[Conversation]:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()
    if conversation:
        db.delete(conversation)
        db.commit()
        return True
    return False


# ---------- MESSAGE ----------

def create_message(db: Session, message_data: MessageCreate) -> Message:
    message = Message(
        conversation_id=message_data.conversation_id,
        sender=message_data.sender,
        content=message_data.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_by_conversation(db: Session, conversation_id: int) -> List[Message]:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

# ---------- MAIL ----------
def update_user_password(db: Session, user_id: int, new_hashed_password: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.hashed_password = new_hashed_password
        db.commit()
        db.refresh(user)
    return user