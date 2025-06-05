"""
Fichier : routes.py (dossier chat)
----------------------------------

Ce module définit les routes liées au système de messagerie (chat) de l'application.

Routes principales :
- POST /chat/conversation : Crée une nouvelle conversation (titre requis).
- GET /chat/conversations : Récupère toutes les conversations de l’utilisateur connecté.
- POST /chat/send-message : Ajoute un message à une conversation existante.
- GET /chat/messages/{conversation_id} : Récupère les messages d’une conversation donnée.
- DELETE /chat/conversations/{conversation_id} : Supprime une conversation appartenant à l’utilisateur.

Dépendances :
- FastAPI : pour la déclaration des routes et l’injection de dépendances (`Depends`).
- SQLAlchemy ORM : pour les opérations CRUD sur la base de données.
- Schémas Pydantic (`schemas`) : pour valider les entrées/sorties.
- Authentification :
    - `get_current_user()` : protège chaque route pour qu’elle soit accessible uniquement à un utilisateur authentifié.
    - `get_db()` : fournit une session de base de données.

Fonctionnalité clé :
Toutes les opérations sont restreintes à l'utilisateur connecté. Cela garantit que les utilisateurs ne peuvent interagir qu’avec leurs propres conversations.

Exemple :
```http
POST /chat/send-message
{
  "conversation_id": 1,
  "sender": "user",
  "content": "Bonjour",
  "is_ai": false
}
"""

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