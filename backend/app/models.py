"""
Fichier : models.py
-------------------

Définition des modèles SQLAlchemy représentant les entités principales de la base de données.

Modèles inclus :
- User : Représente un utilisateur avec email, mot de passe haché et date de création.
- Conversation : Représente une conversation liée à un utilisateur, avec un titre et une date de création.
- Message : Représente un message d’une conversation, avec expéditeur, contenu, date et indicateur IA.

Relations principales :
- Un User peut avoir plusieurs Conversations.
- Une Conversation appartient à un User et contient plusieurs Messages.
- Un Message appartient à une Conversation.

Caractéristiques techniques :
- Utilisation des types SQLAlchemy (Integer, String, DateTime, Boolean).
- Relations ORM avec back_populates pour navigabilité bidirectionnelle.
- Cascade sur les messages pour suppression automatique lors de suppression de conversation.
- Dates de création avec valeurs par défaut (UTC et fonction SQL NOW).

Remarques :
- Ces modèles sont la base de la couche ORM utilisée dans l’application.
- La synchronisation avec la base est gérée via `Base.metadata.create_all`.
"""




from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from sqlalchemy import Boolean, func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    is_ai = Column(Boolean, default=False, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")

