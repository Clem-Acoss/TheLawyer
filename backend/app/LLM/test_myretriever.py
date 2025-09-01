# app/LLM/test_myretriever.py

from retriever_service import MyVectorDBRetriever
from llama_index.vector_stores.postgres import PGVectorStore  # ou l'import correct de ton PGVectorStore
import os

# === CONFIG ===
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

VECTOR_TABLE = "cra_assist_vector_store_boss"  # ou la table que tu veux tester
QUERY = "exonération des apprentis"
TOP_K = 5

def test_retriever():
    # 1️⃣ Initialise le vector store
    vector_store = PGVectorStore.from_params(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        table_name=VECTOR_TABLE,
        embed_dim=896
    )

    # 2️⃣ Initialise ton retriever
    retriever = MyVectorDBRetriever(
        vector_store,
        embed_model="local",
        query_mode="default",
        similarity_top_k=TOP_K
    )

    # 3️⃣ Récupère les nodes
    nodes = retriever.retrieve(QUERY)

    # 4️⃣ Affiche le résultat
    print(f">>> Nombre de chunks trouvés : {len(nodes)}")
    for i, n in enumerate(nodes, 1):
        print(f"\n--- Chunk {i} (score={n.score}) ---")
        print(n.node.get_content()[:300])  # affiche un extrait de 300 caractères

    return nodes

if __name__ == "__main__":
    test_retriever()
