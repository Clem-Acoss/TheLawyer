import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
OLLAMA_URL = "http://localhost:11434/api/generate"

# Définition du corpus statique (ou charger depuis un fichier si nécessaire)
corpus = [
    "La France est un pays d'Europe.",
    "Paris est la capitale de la France.",
    "Le vin français est réputé dans le monde.",
    "La Tour Eiffel est un monument célèbre à Paris.",
    "Les fromages français sont variés et délicieux."
]

# Chargement du modèle d'embedder
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
corpus_embeddings = embedder.encode(corpus, convert_to_numpy=True)

dimension = corpus_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(corpus_embeddings)


def search_documents(query: str, k: int = 3) -> list[str]:
    """
    Retourne les k documents les plus proches de la requête.
    """
    query_vec = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, k)
    return [corpus[i] for i in indices[0]]


def generate_answer(question: str, context_docs: list[str]) -> str:
    """
    Appelle Ollama local pour générer la réponse en contexte RAG.
    """
    context = "\n".join(context_docs)
    prompt = f"Contexte : {context}\nQuestion : {question}\nRéponse :"

    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    if resp.status_code == 200:
        return resp.json().get("response", "")
    else:
        return f"Erreur API ({resp.status_code}): {resp.text}"


def ask_question_pipeline(user_id: int, title: str, question: str, k: int = 3) -> dict:
    """
    1) Recherche k docs via FAISS
    2) Génération Ollama
    3) Enregistrement question + réponse dans le CSV
    """
    # 1. Recherche
    docs = search_documents(question, k)

    # 2. Génération
    answer = generate_answer(question, docs)

    # 3. Enregistrement
    from db.crud import add_message
    timestamp = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_message(user_id, title, question, timestamp)
    add_message(user_id, title, answer, timestamp)

    # 4. Retour
    return {"question": question, "context": docs, "answer": answer}