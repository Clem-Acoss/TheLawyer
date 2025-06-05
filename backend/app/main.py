
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



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.chat.routes import router as chat_router
from app.LLM import routes as llm_routes
from app.LLM import rag_service
from app.database import Base, engine

# Création des tables
Base.metadata.create_all(bind=engine)

# Création de l'app FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Routers
app.include_router(rag_service.router, prefix="/rag", tags=["RAG"])
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(llm_routes.router)

