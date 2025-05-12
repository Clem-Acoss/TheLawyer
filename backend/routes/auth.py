# backend/routes/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import csv
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Schéma des données reçues
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):

    email: str
    password: str

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'users.csv')

@router.post("/register")
async def register(user: dict):
    # Assure que le fichier existe
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "name", "email", "password"])  # Header

    # Récupère le dernier user_id
    last_user_id = 0
    with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                last_user_id = max(last_user_id, int(row["user_id"]))
            except (ValueError, KeyError):
                continue

    new_user_id = last_user_id + 1

    # Vérifie que l'email n'existe pas déjà
    with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if any(row["email"] == user["email"] for row in reader):
            raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    # Ajoute le nouvel utilisateur
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([new_user_id, user["name"], user["email"], user["password"]])

    return {"message": "Compte créé avec succès", "user_id": new_user_id}

@router.post("/login")
async def login_user(user: UserLogin):
    file_exists = os.path.isfile(CSV_FILE_PATH)
    
    print(f"File exists: {file_exists}")

    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                if row["email"] == user.email and row["password"] == user.password:
                    return {
                        "message": "Connexion réussie",
                        "user_id": idx + 1  # retourne l'index comme user_id (⚠️ simplifié)
                    }
            raise HTTPException(status_code=401, detail="Identifiants invalides")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier d'utilisateurs non trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
