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
    allow_origins=["http://localhost:8080"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lancement vectorisation PDF à démarrage

# Routers
app.include_router(rag_service.router, prefix="/rag", tags=["RAG"])
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(llm_routes.router)

