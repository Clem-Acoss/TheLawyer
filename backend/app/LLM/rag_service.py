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
from app import crud, models, schemas
from app.auth.deps import get_db, get_current_user
from app.schemas import QuestionRequest, MessageOut, MessageCreate
from app.config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, DB_PORT
from app.LLM.llm_service import OurLLM

from app.LLM.retriever_service import MyVectorDBRetriever
from unstructured.staging.base import elements_from_base64_gzipped_json
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from app.config import (
    DATABASE_URL,
    DB_NAME,
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    
)

DATABASE_URL = os.getenv("DATABASE_URL")
PGVECTOR_TABLE = os.getenv("PGVECTOR_TABLE", "documents")

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

router = APIRouter()

# --- Connexion PG ---
def get_pg_connection():
    return psycopg2.connect(
        db_name=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# --- Extraction texte du PDF ---
'''
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
'''
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
'''
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
'''

def get_response_from_RAG(user_query: str, data_source="cra_assist_vector_store_boss", chunks_number=10):
    try:
        # define the vector store
        vector_store = PGVectorStore.from_params(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            table_name=data_source,
            embed_dim=896
        )
        print("[RAG] Vector store initialisé OK")
    except Exception as e:
        import traceback
        print("[RAG][ERROR] Impossible d'initialiser le vector store :")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur initialisation vector store : {str(e)}")

    print("[RAG] Initialisation LLM...")
    try:
        Settings.llm = OurLLM()
    except Exception as e:
        import traceback
        print("[RAG][ERROR] Erreur LLM :", e)
        print(traceback.format_exc())
        raise
    print("[RAG] LLM initialisé OK")

    print("[RAG] Initialisation du retriever...")
    try:
        retriever = MyVectorDBRetriever(
            vector_store,
            embed_model="local",
            query_mode="default",
            similarity_top_k=chunks_number
        )
        print("[RAG] Retriever OK")

        llm_instance = Settings.llm
        print("[RAG] Création du query engine...")
        query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm_instance)
        print("[RAG] Query engine OK")
    except Exception as e:
        import traceback
        print("[RAG][ERROR] Impossible d'initialiser le retriever ou le query engine :")
        print(e)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur initialisation retriever/query engine : {str(e)}"
        )

    print(f"[RAG] Envoi de la requête : {user_query}")
    try:
        response = query_engine.query(user_query)
        print("[RAG] Réponse brute reçue")
        print(">>> Source nodes trouvés :", len(response.source_nodes))
        for s in response.source_nodes:
            print(">>> Chunk:", s.node.get_content()[:200], "... score:", s.score)
    except Exception as e:
        import traceback
        print("[RAG][ERROR] Erreur lors de la requête au query engine :")
        print(e)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la requête RAG : {str(e)}"
        )

    # --- Normalisation des chunks pour le frontend ---
    chunks_metadata = []
    for node_with_score in response.source_nodes:
        node_dict = node_with_score.node.to_dict()
        node_dict["score"] = node_with_score.score
        node_dict["metadata"]["orig_elements"] = [
            {orig_element.category: orig_element.text}
            for orig_element in elements_from_base64_gzipped_json(node_dict["metadata"]["orig_elements"])
        ]

        # Mapping pour frontend : node_text
        chunks_metadata.append({
            "node_text": node_dict.get("text") or node_dict.get("content") or "",
            "score": node_dict["score"],
            "metadata": node_dict.get("metadata", {})
        })

    api_response = {
        "answer": response.response,
        "chunks_metadata": chunks_metadata
    }

    print("[RAG] Réponse formatée et prête")
    print(">>> Type de la réponse :", type(response))
    print(">>> Contenu brut de response :", response)
    print(">>> dir(response):", dir(response))
    return api_response
# === ROUTE ASK (avec session_id déjà existant) ===
@router.post("/ask", response_model=schemas.MessageOut)
def ask_rag(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    question = request.question
    conversation_id = request.conversation_id
    data_source = request.data_source 

    # Mapping front -> nom réel de la table
    SOURCE_TABLE_MAP = {
        "urssaf": "cra_assist_vector_store_urssaf_fr",
        "lamy": "cra_assist_vector_store_LAMY",
        "legifrance": "cra_assist_vector_store_LEGIFRANCE",
        "boss": "cra_assist_vector_store_boss",
    }

    data_source_table = SOURCE_TABLE_MAP.get(data_source.lower())
    if not data_source_table:
        raise HTTPException(status_code=400, detail=f"Data source inconnue: {data_source}")

    # Sauvegarde du message utilisateur
    user_message_data = schemas.MessageCreate(
        conversation_id=conversation_id,
        sender="user",
        content=question,
        is_ai=False,
    )
    crud.create_message(db=db, message_data=user_message_data)

    # 🔹 Appel RAG
    try:
        rag_result = get_response_from_RAG(
            user_query=question,
            data_source=data_source_table,
            chunks_number=10
        )

        # Récupération du texte de la réponse et des chunks directement depuis le dict
        response_text = rag_result.get("answer", "")
        chunks_metadata = rag_result.get("chunks_metadata", [])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur RAG : {str(e)}")

    # Sauvegarde message IA avec chunks
    ai_message_data = schemas.MessageCreate(
        conversation_id=conversation_id,
        sender="assistant",
        content=response_text,
        is_ai=True,
        chunks=chunks_metadata
    )
    print("[DEBUG urgennnnnnnnnnt] chunks_metadata:", chunks_metadata)
    ai_message = crud.create_message(db=db, message_data=ai_message_data)

    return {
        "id": ai_message.id,
        "sender": ai_message.sender,
        "content": ai_message.content,
        "created_at": ai_message.created_at.isoformat(),
        "is_ai": ai_message.is_ai,
        "chunks": ai_message.chunks or []
    }




# === ROUTE ASK-WITH-PDF (upload + index temporaire) ===
'''

@router.post("/ask-with-pdf", response_model=schemas.MessageOut)
def ask_rag(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    question = request.question
    conversation_id = request.conversation_id
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
'''