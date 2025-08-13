
# retriever_service.py

from typing import List, Optional
from llama_index.core.schema import QueryBundle, NodeWithScore
from llama_index.core.vector_stores.types import VectorStoreQuery
from app.models import VectorDBRetriever  
import requests
import os

EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")
EMBEDDING_API_TOKEN = os.getenv("EMBEDDING_API_TOKEN")



def _query_embedding(self, texts: list):

    headers = {
        "Authorization": f"Bearer {EMBEDDING_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"inputs": texts, "options": {}}
    response = requests.post(EMBEDDING_API_URL, headers=headers, json=data, verify=False)
    if response.status_code != 200:
        raise Exception(f"Embedding API request failed: {response.status_code} - {response.text}")
    return response.json()  

def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
    query_embedding = self._query_embedding([query_bundle.query_str])[0]

    vector_store_query = VectorStoreQuery(
        query_embedding=query_embedding,
        similarity_top_k=self._similarity_top_k,
        mode=self._query_mode,
    )
    query_result = self._vector_store.query(vector_store_query)

    nodes_with_scores = []
    for index, node in enumerate(query_result.nodes):
        score: Optional[float] = None
        if query_result.similarities is not None:
            score = query_result.similarities[index]
        nodes_with_scores.append(NodeWithScore(node=node, score=score))

    return nodes_with_scores


class MyVectorDBRetriever(VectorDBRetriever):
    _query_embedding = _query_embedding
    _retrieve = _retrieve