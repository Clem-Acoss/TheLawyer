
# embedding_service.py

import os
import requests
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis le .env

API_URL = os.getenv("EMBEDDING_API_URL")
API_TOKEN = os.getenv("EMBEDDING_API_TOKEN")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_embeddings(texts):
    payload = {

        "inputs": texts ,
        "options": {}
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload), verify=False)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code} - {response.text}")

    # On suppose que l'API renvoie {"embeddings": [[...], [...]]}
  
    embeddings = response.json()
    return np.array(embeddings, dtype="float32")
