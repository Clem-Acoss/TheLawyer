
"""
Fichier : service.py (dossier chat)
-----------------------------------

Ce module regroupe la logique métier liée aux conversations et aux messages (chat).

Fonctions :
- create_conversation(db, user_id, title) :
    Crée une nouvelle conversation pour un utilisateur donné.
    Paramètres : ID de l'utilisateur, titre de la conversation.

- get_conversations(db, user_id) :
    Récupère toutes les conversations appartenant à un utilisateur.

- add_message(db, conversation_id, sender, content, is_ai=False) :
    Ajoute un message dans une conversation spécifique.
    Le message peut être envoyé par un humain ou une IA (`is_ai=True`).

- get_messages(db, conversation_id) :
    Récupère tous les messages liés à une conversation donnée.

Dépendances :
- SQLAlchemy ORM : pour interagir avec les tables `Conversation` et `Message` définies dans `models`.
- Pas de validation ici : les données sont supposées déjà validées par les schémas Pydantic (côté routes).

Responsabilité :
Ce fichier agit comme couche de service intermédiaire entre les routes (`routes.py`) et la base de données (`models.py`).

Exemple de création de message :
```python
add_message(db, conversation_id=3, sender="user", content="Bonjour", is_ai=False)
"""


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

def add_message(db: Session, conversation_id: int, sender: str, content: str, is_ai: bool = False):
    msg = models.Message(
        conversation_id=conversation_id,
        sender=sender,
        content=content,
        is_ai=is_ai
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, conversation_id: int):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
