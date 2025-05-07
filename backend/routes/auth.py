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
async def register_user(user: UserRegister):
    file_exists = os.path.isfile(CSV_FILE_PATH)
    console.log(f"File exists: {file_exists}")
    print(f"File exists: {file_exists}")

    try:
        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "email", "password"])

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                
                "name": user.name,
                "email": user.email,
                "password": user.password,  # ⚠️ à sécuriser plus tard
            })

        return {"message": "Utilisateur enregistré avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(user: UserLogin):
    file_exists = os.path.isfile(CSV_FILE_PATH)
    
    print(f"File exists: {file_exists}")

    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["email"] == user.email and row["password"] == user.password:
                    return {"message": "Connexion réussie"}
            raise HTTPException(status_code=401, detail="Identifiants invalides")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier d'utilisateurs non trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))