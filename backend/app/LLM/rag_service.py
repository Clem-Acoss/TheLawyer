from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import fitz  # PyMuPDF
import faiss
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer
import requests

from app.schemas import QuestionRequest, MessageOut, MessageCreate
from app.auth.deps import get_db, get_current_user
from app import crud, models

router = APIRouter()

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
        print(f"[❌] PDF introuvable : {PDF_PATH}")
        return

    with fitz.open(PDF_PATH) as pdf:
        full_text = "\n".join([page.get_text() for page in pdf])

    if not full_text.strip():
        full_text = extract_text_with_ocr(PDF_PATH)

    if not full_text.strip():
        print("[🚫] Texte vide après OCR.")
        return

    chunks = split_text(full_text)
    embeddings = embedder.encode(chunks, show_progress_bar=True)

    for chunk, vector in zip(chunks, embeddings):
        index.add(np.array([vector], dtype='float32'))
        chunks_list.append(chunk)

@router.on_event("startup")
def startup_event():
    initialize_rag()


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

    # 👉 1. Enregistrer le message de l'utilisateur dans la base
    user_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="user",
        content=question,
        is_ai=False
    )
    crud.create_message(db=db, message_data=user_message_data)

    # 👉 2. Construire le prompt pour le RAG
    question_vector = embedder.encode([question])[0].astype("float32")
    _, I = index.search(np.array([question_vector]), k=5)
    top_chunks = [chunks_list[i] for i in I[0] if i < len(chunks_list)]
    context = "\n\n".join(top_chunks)

    prompt = f"""Voici des extraits juridiques :
{context}

Question : {question}
Réponse :"""

    # 👉 3. Appeler le modèle
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

    # 👉 4. Enregistrer la réponse IA
    ai_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="assistant",
        content=response,
        is_ai=True
    )
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    # 👉 5. Retourner la réponse IA (tu pourrais aussi retourner les 2 si besoin)
    return ai_message
