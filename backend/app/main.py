"""
Fichier : main.py
-----------------

Ce module initialise et configure l’application FastAPI principale.

Il inclut :
- La création de l’instance FastAPI
- La configuration du middleware CORS pour autoriser le frontend
- L’initialisation de la base de données (création des tables)
- L’enregistrement des routes (authentification, chat, LLM, RAG)

Fonctionnalités principales :
- Gestion des requêtes API via les différents routers
- Sécurisation CORS pour permettre les appels depuis le frontend local
- Chargement automatique des modèles et services nécessaires au démarrage

Remarques :
- Le serveur doit être démarré avec `uvicorn app.main:app`
- La vectorisation PDF et indexation RAG peuvent être lancées au démarrage via le router `rag_service`
- Le backend supporte plusieurs modules fonctionnels (auth, chat, LLM, RAG) de manière modulaire
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.auth.routes import router as auth_router
from app.chat.routes import router as chat_router
from app.LLM import routes as llm_routes
from app.LLM import rag_service
from app.database import Base, engine

# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:8080",
        "http://0.0.0.0:8000",
        "http://0.0.0.0:8080",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers API
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(rag_service.router, prefix="/rag", tags=["RAG"])
#app.include_router(llm_routes.router)

# === FRONTEND (React) ===

# Chemin vers le dossier `static/` (build React)
frontend_dist_path = os.path.join(os.path.dirname(__file__), "static")
assets_path = os.path.join(frontend_dist_path, "assets")

# 1. Sert les fichiers /assets/... (JS, CSS, fonts, etc.)
if os.path.isdir(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# 2. Sert le dossier React build (pour favicon, manifest...)
app.mount("/static", StaticFiles(directory=frontend_dist_path), name="static_root")

# 3. Catch-all pour React Router (SPA)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "index.html non trouvé"}
