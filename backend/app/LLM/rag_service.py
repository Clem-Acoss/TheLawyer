"""
Fichier : rag_service.py (module LLM/RAG)
-----------------------------------------

Ce module gère le pipeline complet du Retrieval-Augmented Generation (RAG) pour l’assistant juridique.

Il inclut :
- L'initialisation du corpus vectorisé depuis un PDF (OCR inclus si besoin)
- L’indexation FAISS avec `SentenceTransformer`
- La récupération des chunks les plus pertinents
- La construction d’un prompt pour le modèle LLaMA
- L’appel à Ollama pour la génération de la réponse
- L’enregistrement des messages (utilisateur et IA) en base

Fonctionnalités clés :
- `/ask` : Pose une question en utilisant un PDF déjà chargé (au démarrage).
- `/ask-with-pdf` : Pose une question en joignant dynamiquement un PDF à indexer.

Composants principaux :
- `fitz` (PyMuPDF) + `pytesseract` : extraction texte ou OCR depuis PDF
- `faiss` : moteur de recherche vectorielle en mémoire
- `SentenceTransformer("all-MiniLM-L6-v2")` : encodeur pour créer les embeddings
- `chunks_list` : stocke les extraits textuels alignés avec FAISS

Remarques :
- Le fichier PDF principal est défini par `PDF_PATH`.
- Le moteur FAISS et les chunks sont globaux et en mémoire (volatiles).
- Lors de l'appel RAG, la base PostgreSQL est utilisée pour stocker les messages.

Exemples :
- `/ask` :
```json
{
  "question": "Quelles sont les exonérations liées au contrat d'apprentissage ?",
  "conversation_id": 3
}
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import fitz  
import faiss
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer
import requests
from fastapi import UploadFile, File, Form
from app.schemas import QuestionRequest, MessageOut, MessageCreate
from app.auth.deps import get_db, get_current_user
from app import crud, models
import uuid
import shutil
router = APIRouter()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# === CONFIGURATION ===
PDF_PATH = "/Users/clementgardair/AcossDev/TheLawyer/Exonération contrat d'apprentissage (1).pdf"
DIM = 384
embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(DIM)
chunks_list = []


# === UTILS ===
def split_text(text, chunk_size=300, overlap=30):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    ocr_text = ""
    for img in images:
        ocr_text += pytesseract.image_to_string(img, lang='fra') + "\n"
    return ocr_text



# === INITIALISATION RAG ===
def initialize_rag():
    if not os.path.exists(PDF_PATH):
        print(f"[!!] PDF introuvable : {PDF_PATH}")
        return

    with fitz.open(PDF_PATH) as pdf:
        full_text = "\n".join([page.get_text() for page in pdf])

    if not full_text.strip():
        full_text = extract_text_with_ocr(PDF_PATH)

    if not full_text.strip():
        print("[!!] Texte vide après OCR.")
        return

    chunks = split_text(full_text)
    embeddings = embedder.encode(chunks, show_progress_bar=True)

    for chunk, vector in zip(chunks, embeddings):
        index.add(np.array([vector], dtype='float32'))
        chunks_list.append(chunk)

@router.on_event("startup")
def startup_event():
    initialize_rag()

def add_pdf_to_rag(pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF introuvable : {pdf_path}")

    with fitz.open(pdf_path) as pdf:
        full_text = "\n".join([page.get_text() for page in pdf])

    if not full_text.strip():
        full_text = extract_text_with_ocr(pdf_path)

    if not full_text.strip():
        raise ValueError("Texte vide après OCR.")

    chunks = split_text(full_text)
    embeddings = embedder.encode(chunks, show_progress_bar=True)

    for chunk, vector in zip(chunks, embeddings):
        index.add(np.array([vector], dtype='float32'))
        chunks_list.append(chunk)

    print(f"[✔️] PDF indexé avec {len(chunks)} chunks.")



# === ROUTE MODIFIÉE ===
@router.post("/ask", response_model=MessageOut)
def ask_rag(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    question = request.question
    conversation_id = request.conversation_id

    if index.ntotal == 0:
        raise HTTPException(status_code=500, detail="Index vectoriel vide.")

    
    user_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="user",
        content=question,
        is_ai=False
    )
    crud.create_message(db=db, message_data=user_message_data)

   
    question_vector = embedder.encode([question])[0].astype("float32")
    _, I = index.search(np.array([question_vector]), k=5)
    top_chunks = [chunks_list[i] for i in I[0] if i < len(chunks_list)]
    context = "\n\n".join(top_chunks)

    prompt = f"""Voici des extraits juridiques :
{context}

Question : {question}
Réponse :"""

   
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=60
        )
        res.raise_for_status()
        response = res.json().get("response", "[Réponse vide]")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    ai_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="assistant",
        content=response,
        is_ai=True
    )
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    
    return ai_message
@router.post("/ask-with-pdf", response_model=MessageOut)
async def ask_with_pdf(
    question: str = Form(...),
    conversation_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
   
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

    
    user_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="user",
        content=question,
        is_ai=False
    )
    crud.create_message(db=db, message_data=user_message_data)

    
    if index.ntotal == 0:
        raise HTTPException(status_code=500, detail="Index vectoriel vide.")

    question_vector = embedder.encode([question])[0].astype("float32")
    _, I = index.search(np.array([question_vector]), k=5)
    top_chunks = [chunks_list[i] for i in I[0] if i < len(chunks_list)]
    context = "\n\n".join(top_chunks)

    prompt = f"""reponse à la question en utilisant les extraits suivants :
{context}

Question : {question}
Réponse :"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=60
        )
        res.raise_for_status()
        response = res.json().get("response", "[Réponse vide]")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

   
    ai_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="assistant",
        content=response,
        is_ai=True
    )
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    
    return ai_message