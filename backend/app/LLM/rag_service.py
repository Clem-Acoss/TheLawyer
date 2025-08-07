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
import pickle
import pytesseract
from pdf2image import convert_from_path
from app.LLM.embedding_service import get_embeddings
import requests
from fastapi import UploadFile, File, Form
from app.schemas import QuestionRequest, MessageOut, MessageCreate
from app.auth.deps import get_db, get_current_user
from app import crud, models
from dotenv import load_dotenv
import uuid
import traceback
import shutil
router = APIRouter()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()  # charge le fichier .env dans os.environ

DATABASE_URL = os.getenv("DATABASE_URL")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")
EMBEDDING_API_TOKEN = os.getenv("EMBEDDING_API_TOKEN")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

# === CONFIGURATION ===
PDF_DIR ="//app//app//Boss"
DIM = 384
index = faiss.IndexFlatL2(DIM)
chunks_list = []
FAISS_INDEX_PATH = "./rag_state/index.faiss"
CHUNKS_PATH = "./rag_state/chunks.pkl"

# === UTILS ===
def split_text(text, chunk_size=200, overlap=30):
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

def save_rag_state():
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(CHUNKS_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks_list, f)

def load_rag_state():
    global index, chunks_list
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            chunks_list = pickle.load(f)
        print(f"[INFO] Index et chunks chargés depuis le disque ({index.ntotal} vecteurs)")
        return True
    return False

# === INITIALISATION RAG ===
def initialize_rag():
    global index, chunks_list

    print("[INIT] Initialisation du RAG multi-PDF...")

    if load_rag_state():
        print("[INIT] État RAG rechargé depuis les fichiers. Aucune indexation nécessaire.")
        return

    if not os.path.exists(PDF_DIR):
        print(f"[!!] Dossier introuvable : {PDF_DIR}")
        return

    all_chunks = []
    all_embeddings = []

    for filename in os.listdir(PDF_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_DIR, filename)
        print(f"[INFO] Traitement du fichier : {filename}")

        try:
            with fitz.open(pdf_path) as pdf:
                full_text = "\n".join([page.get_text() for page in pdf])
        except Exception as e:
            print(f"[WARN] Impossible de lire {filename} avec PyMuPDF : {e}")
            continue

        if not full_text.strip():
            print(f"[INFO] Aucun texte détecté dans {filename}, tentative OCR...")
            try:
                full_text = extract_text_with_ocr(pdf_path)
            except Exception as e:
                print(f"[WARN] OCR échoué pour {filename} : {e}")
                continue

        if not full_text.strip():
            print(f"[WARN] Texte vide même après OCR pour {filename}, ignoré.")
            continue

        chunks = split_text(full_text)
        BATCH_SIZE = 100  # Ajuste selon la taille acceptable pour l’API
        embeddings = []

        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i:i + BATCH_SIZE]
        try:
            batch_embeddings = get_embeddings(batch)
            embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"[WARN] Échec d'embedding pour le batch {i}–{i+BATCH_SIZE}: {e}")


        if embeddings is None or len(embeddings) == 0:
            print(f"[WARN] Aucun embedding généré pour {filename}, ignoré.")
            continue

        all_chunks.extend(chunks)
        all_embeddings.extend(embeddings)

    if not all_embeddings:
        print("[!!] Aucun embedding généré pour les PDF du dossier.")
        return

    dimension = len(all_embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    print(f"[INFO] Création de l'index avec {len(all_chunks)} chunks...")
    for chunk, vector in zip(all_chunks, all_embeddings):
        index.add(np.array([vector], dtype='float32'))

    chunks_list.extend(all_chunks)

    print(f"[INFO] Index FAISS construit avec {index.ntotal} vecteurs.")
    save_rag_state()
    print("[INFO] État RAG sauvegardé.")



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
    embeddings = get_embeddings(chunks)

    tmp_index = faiss.IndexFlatL2(len(embeddings[0]))
    for vector in embeddings:
        tmp_index.add(np.array([vector], dtype='float32'))

    return tmp_index, chunks

# === ROUTE MODIFIÉE ===
@router.post("/ask", response_model=MessageOut)
def ask_rag(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    question = request.question
    conversation_id = request.conversation_id

    print("[DEBUG] Appel à get_answer_from_rag")
    print(f"[DEBUG] Question : {question}")
    print(f"[DEBUG] Taille de l'index : {index.ntotal if index else 'Index non initialisé'}")
    print(f"[DEBUG] Nombre de chunks : {len(chunks_list) if chunks_list else 'chunks_list vide ou non initialisée'}")

    if index.ntotal == 0:
        raise HTTPException(status_code=500, detail="Index vectoriel vide.")

    
    user_message_data = MessageCreate(
        conversation_id=conversation_id,
        sender="user",
        content=question,
        is_ai=False
    )
    crud.create_message(db=db, message_data=user_message_data)

   
    question_vector = get_embeddings([question])[0]
    print(f"[DEBUG] Type : {type(question_vector)}, longueur : {len(question_vector)}")
    _, I = index.search(np.array([question_vector]), k=5)
    top_chunks = [chunks_list[i] for i in I[0] if i < len(chunks_list)]
    context = "\n\n".join(top_chunks)

    prompt = f"""
    Tu es un assistant juridique. Réponds à la question suivante en t'appuyant sur les extraits ci-dessous, ne prends pas en compte ce qui n'a aucun rapport avec la question. 

    Formate ta réponse de façon claire et lisible, en utilisant des **titres**, des **puces** ou des **listes numérotées** si nécessaire. Utilise le **Markdown** pour la mise en forme.

    ---

    ### Contexte :
    {context}

    ---

    ### Question :
    {question}

    ---

    ### Réponse :
    """

   
    try:
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}", 
            "Content-Type": "application/json"
        }
        url = LLM_API_URL
        data = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }

        res = requests.post(url, headers=headers, json=data, verify=False, timeout=60)
        res.raise_for_status()
        response = res.json()["choices"][0]["message"]["content"]

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
        tmp_index, tmp_chunks = add_pdf_to_rag(tmp_path)

        print("[INFO] Création du message utilisateur...")
        user_message_data = MessageCreate(
            conversation_id=conversation_id,
            sender="user",
            content=question,
            is_ai=False
        )
        crud.create_message(db=db, message_data=user_message_data)

        if tmp_index.ntotal == 0:
            print("[ERROR] L'index vectoriel est vide.")
            raise HTTPException(status_code=500, detail="Index vectoriel vide.")

        print("[INFO] Génération du vecteur de question...")
        question_vector = get_embeddings([question])[0]
        _, I = tmp_index.search(np.array([question_vector]), k=5)
        top_chunks = [tmp_chunks[i] for i in I[0] if i < len(tmp_chunks)]
        context = "\n\n".join(top_chunks)

        print("[INFO] Construction du prompt LLM...")
        prompt = f"""Réponds à la question en utilisant uniquement les extraits suivants :
{context}

Question : {question}
Réponse :"""

        print("[INFO] Envoi de la requête au LLM...")
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }

        res = requests.post(
            LLM_API_URL,
            headers=headers,
            json=data,
            verify=False,
            timeout=60
        )
        res.raise_for_status()
        response = res.json()["choices"][0]["message"]["content"]
        print("[INFO] Réponse LLM reçue.")

        print("[INFO] Sauvegarde du message de l'assistant...")
        ai_message_data = MessageCreate(
            conversation_id=conversation_id,
            sender="assistant",
            content=response,
            is_ai=True
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
            print(f"[WARN] Impossible de supprimer le fichier temporaire : {cleanup_err}")