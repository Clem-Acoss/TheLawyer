# llm_service.py
import json
import requests
from typing import Any
import os
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.llms import CompletionResponse, CompletionResponseGen
from app.models import OurLLM as BaseOurLLM

# Variables d’environnement
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL")


def _query_llm(self, query: str) -> str:
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": query}],
    }
    response = requests.post(LLM_API_URL, headers=headers, json=payload, verify=False)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


@llm_completion_callback()
def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
    text = self._query_llm(prompt)
    return CompletionResponse(text=text)


@llm_completion_callback()
def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
    # Si ton API ne supporte pas le streaming, on "simule"
    text = self._query_llm(prompt)
    for token in text.split():
        yield CompletionResponse(text=token, delta=token)


# Sous-classe concrète pour que Python ne la considère plus comme abstraite
class OurLLM(BaseOurLLM):
    _query_llm = _query_llm
    complete = complete
    stream_complete = stream_complete
