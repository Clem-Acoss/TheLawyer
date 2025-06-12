"""
Fichier : routes.py (module LLM)
--------------------------------

Ce module définit les routes FastAPI pour l’interaction avec le modèle LLaMA local (hors RAG)
et pour l’indexation manuelle de fichiers PDF dans le système RAG.

Il inclut :
- Un endpoint `/chat/send-message-llm` pour envoyer un message simple au modèle LLaMA3.2 via Ollama
- Un endpoint `/upload-pdf` pour charger et indexer un fichier PDF dans le moteur FAISS
- L’inclusion des routes RAG depuis `rag_service.py` via `/rag`

Fonctionnalités clés :
- Enregistrement automatique des messages utilisateur et IA dans la base PostgreSQL
- Utilisation d’Ollama local pour générer une réponse à partir d’un prompt brut
- Gestion de l’upload de fichiers PDF, avec indexation vectorielle

Composants principaux :
- `requests` : pour interagir avec l’API Ollama (`localhost:11434`)
- `shutil`, `uuid`, `os` : pour gérer les fichiers PDF temporairement
- `rag_service` : import de la fonction `add_pdf_to_rag` et des routes

Remarques :
- Le PDF est temporairement stocké dans `/tmp/uploads` avant d’être indexé
- L’indexation utilise FAISS et SentenceTransformer, gérés dans `rag_service.py`
- Le modèle utilisé est défini dans l’appel à l’API Ollama (`model: llama3.2`)
"""

from fastapi import UploadFile, File, HTTPException
from app.LLM.rag_service import add_pdf_to_rag
from app.LLM import rag_service
import shutil
import uuid
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
from app.schemas import MessageRequest, MessageOut
from app.auth.deps import get_db
from app import crud, models
from app.auth.deps import get_current_user
from app.schemas import MessageCreate
router = APIRouter()
router.include_router(rag_service.router, prefix="/rag")

@router.post("/chat/send-message-llm", response_model=MessageOut)
def send_message_llm(
    request: MessageRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_message_data = MessageCreate(
        conversation_id=request.conversation_id,
        sender=request.sender,
        content=request.content,
        is_ai=False
    )
    user_message = crud.create_message(db=db, message_data=user_message_data)

    # Configuration API distante
    api_key = "xxxxxxxxxxx" #mettre son api key 
    url = "https://llama3370b.urssaf.cloud-acoss.fr/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Infermatic/Llama-3.3-70B-Instruct-FP8-Dynamic",
        "messages": [{"role": "user", "content": request.content}],
        # Optionnel : ajouter temperature / max_tokens / top_p si besoin
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur de connexion à l'API distante : {e}")

    try:
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
    except (KeyError, ValueError, IndexError) as e:
        raise RuntimeError(f"Erreur dans la réponse du modèle : {e}")

    ai_message_data = MessageCreate(
        conversation_id=request.conversation_id,
        sender="assistant",
        content=ai_response,
        is_ai=True
    )
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    return ai_message

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")
    
    
    tmp_dir = "/tmp/uploads"
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}.pdf")

    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        add_pdf_to_rag(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'indexation PDF: {str(e)}")

    return {"detail": "PDF ajouté et indexé avec succès"}
