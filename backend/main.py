from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat, auth

app = FastAPI()

# CORS pour React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
