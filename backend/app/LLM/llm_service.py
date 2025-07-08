
#llm_service.py


import requests
import os
import json

def query_llm(query):
    api_key = os.getenv("LLM_API_KEY")
    url = os.getenv("LLM_API_URL")
    model = os.getenv("LLM_MODEL")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": query}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    response.raise_for_status()  # Gestion erreur réseau
    result = response.json()
    return result["choices"][0]["message"]["content"]
