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




from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from sqlalchemy import Boolean, func
from typing import Any
from llama_index.vector_stores.postgres import PGVectorStore
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import UnstructuredReader
from llama_index.core.schema import Document

from llama_index.core import QueryBundle
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore
from llama_index.core.vector_stores import VectorStoreQuery

from typing import Optional, List, Mapping, Any
from llama_index.core import SimpleDirectoryReader, SummaryIndex
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings
from llama_index.core.query_engine import RetrieverQueryEngine


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
    chunks = Column(JSON, nullable=True)
    conversation = relationship("Conversation", back_populates="messages")

class OurLLM(CustomLLM):
    context_window: int = 3900
    num_output: int = 256
    model_name: str = "custom"
    dummy_response: str = "My response"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

class VectorDBRetriever(BaseRetriever):
    

    def __init__(
        self,
        vector_store: PGVectorStore,
        embed_model: Any,
        query_mode: str = "default",
        similarity_top_k: int = 2,
    ) -> None:
        self._vector_store = vector_store
        self._embed_model = embed_model
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k
        super().__init__()