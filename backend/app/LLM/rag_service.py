# rag_service.py - Version PGVector avec upload PDF temporaire
import os
import uuid
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import psycopg2
import traceback
import requests
import numpy as np
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.LLM.embedding_service import get_embeddings
from app import crud, models, schemas
from app.auth.deps import get_db, get_current_user
from app.schemas import QuestionRequest, MessageOut, MessageCreate
from app.config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, DB_PORT

DATABASE_URL = os.getenv("DATABASE_URL")
PGVECTOR_TABLE = os.getenv("PGVECTOR_TABLE", "documents")

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

router = APIRouter()

# --- Connexion PG ---
def get_pg_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# --- Extraction texte du PDF ---
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    pdf = fitz.open(pdf_path)
    for page in pdf:
        page_text = page.get_text()
        if not page_text.strip():  # OCR si pas de texte
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img, lang="fra")
        else:
            text += page_text
    return text.strip()

# --- Découpage en chunks ---
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# --- Ajout PDF dans PGVector ---
def add_pdf_to_rag(pdf_path: str) -> str:
    try:
        session_id = str(uuid.uuid4())
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)

        embeddings = get_embeddings(chunks)

        conn = get_pg_connection()
        cur = conn.cursor()

        for chunk, emb in zip(chunks, embeddings):
            emb_str = "[" + ",".join(str(x) for x in emb) + "]"
            cur.execute(
                f"""
                INSERT INTO {PGVECTOR_TABLE} (session_id, content, embedding)
                VALUES (%s, %s, %s)
                """,
                (session_id, chunk, emb_str)
            )

        conn.commit()
        conn.close()
        return session_id
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur ajout PDF : {str(e)}")

# --- Recherche limitée à un session_id ---
def search_chunks_for_session(question: str, session_id: str, k: int = 20):
    try:
        vector = get_embeddings([question])[0]
        vector_str = "[" + ",".join(str(x) for x in vector) + "]"

        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT text
            FROM {PGVECTOR_TABLE}
            ORDER BY embedding <=> %s
            LIMIT %s
        """, (vector_str, k))
        results = cur.fetchall()
        conn.close()

        return [row[0] for row in results]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur recherche PGVector : {str(e)}")

# === ROUTE ASK (avec session_id déjà existant) ===
@router.post("/ask", response_model=schemas.MessageOut)
def ask_rag(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    question = request.question
    conversation_id = request.conversation_id
    # Si tu as besoin de session_id, il faut la récupérer d'ailleurs, sinon supprime ces lignes
    # session_id = ...

    print(f"[DEBUG] Question : {question}")
    print(f"[DEBUG] Conversation_id : {conversation_id}")

    # Supposons que search_chunks_for_session n'ait pas besoin de session_id mais conversation_id
    top_chunks = search_chunks_for_session(question, conversation_id, k=20)
    if not top_chunks:
        raise HTTPException(status_code=500, detail="Pas de données dans la session RAG.")

    context = "\n\n".join(top_chunks)

    prompt = f"""
    Tu es un assistant juridique. Réponds à la question suivante en t'appuyant sur les extraits ci-dessous, ne prends pas en compte les extraits hors contexte.

    --- Contexte ---
    {context}

    --- Question ---
    {question}

    --- Réponse ---
    """

    user_message_data = schemas.MessageCreate(
        conversation_id=conversation_id,
        sender="user",
        content=question,
        is_ai=False,
    )
    crud.create_message(db=db, message_data=user_message_data)

    # Appel LLM API
    try:
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
        res = requests.post(LLM_API_URL, headers=headers, json=data, verify=False, timeout=60)
        res.raise_for_status()
        response = res.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    ai_message_data = schemas.MessageCreate(
        conversation_id=conversation_id,
        sender="assistant",
        content=response,
        is_ai=True,
    )
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    return ai_message



# === ROUTE ASK-WITH-PDF (upload + index temporaire) ===
@router.post("/ask-with-pdf", response_model=schemas.MessageOut)
def ask_rag(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    print("[INFO] Requête reçue sur /ask-with-pdf")

    if file.content_type != "application/pdf":
        print("[ERROR] Fichier non PDF reçu.")
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")

    tmp_dir = "/tmp/uploads"
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}.pdf")

    try:
        print(f"[INFO] Sauvegarde du fichier temporaire : {tmp_path}")
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("[INFO] Ajout du PDF au RAG...")
        session_id = add_pdf_to_rag(tmp_path)

        print("[INFO] Recherche des chunks...")
        top_chunks = search_chunks_for_session(question, session_id, k=20)
        if not top_chunks:
            raise HTTPException(status_code=500, detail="Index vectoriel vide.")

        context = "\n\n".join(top_chunks)

        print("[INFO] Construction du prompt LLM...")
        prompt = f"""
        Tu es un assistant juridique. Réponds uniquement avec les extraits suivants :

        --- Contexte ---
        {context}

        --- Question ---
        {question}

        --- Réponse ---
        """

        print("[INFO] Création message utilisateur...")
        user_message_data = schemas.MessageCreate(
            conversation_id=conversation_id,
            sender="user",
            content=question,
            is_ai=False,
        )
        crud.create_message(db=db, message_data=user_message_data)

        print("[INFO] Envoi requête au LLM...")
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }

        res = requests.post(LLM_API_URL, headers=headers, json=data, verify=False, timeout=60)
        res.raise_for_status()
        response = res.json()["choices"][0]["message"]["content"]
        print("[INFO] Réponse LLM reçue.")

        print("[INFO] Sauvegarde message assistant...")
        ai_message_data = schemas.MessageCreate(
            conversation_id=conversation_id,
            sender="assistant",
            content=response,
            is_ai=True,
        )
        ai_message = crud.create_message(db=db, message_data=ai_message_data)

        return ai_message

    except Exception as e:
        print(f"[ERROR] Erreur lors du traitement : {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement : {str(e)}")

    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                print("[INFO] Fichier temporaire supprimé.")
        except Exception as cleanup_err:
            print(f"[WARN] Impossible de supprimer fichier temporaire : {cleanup_err}")