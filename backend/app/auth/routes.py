
"""
Fichier : routes.py (dossier auth)
----------------------------------

Ce module définit les routes d'authentification de l'API (inscription et connexion) via FastAPI.

Fonctionnalités :
- /auth/signup : Permet à un nouvel utilisateur de s’inscrire avec email et mot de passe.
- /auth/login  : Permet à un utilisateur existant de se connecter et de recevoir un token JWT.

Détails des routes :
- POST /auth/signup
  - Données : JSON conforme au schéma `UserCreate`
  - Vérifie si l’email existe déjà
  - Hash le mot de passe et crée un utilisateur en base
  - Réponse : objet `UserOut` (sans le mot de passe)

- POST /auth/login
  - Données : `OAuth2PasswordRequestForm` (username + password)
  - Vérifie l’identité (email et mot de passe hashé)
  - Génère un JWT signé contenant l’ID de l’utilisateur
  - Réponse : access_token + token_type ("bearer")

Dépendances :
- FastAPI : gestion des routes et exceptions
- SQLAlchemy : session DB
- Schémas : `UserCreate`, `UserOut`, `Token`
- Utils : fonctions de hash, vérification du mot de passe, génération de token
- Dépendance `get_db` pour injecter la session DB

Utilisation :
Ces routes sont utilisées par le frontend pour inscrire ou authentifier les utilisateurs,
et pour obtenir le token JWT nécessaire à l’accès aux routes sécurisées.

Exemple d’appel (POST /auth/login) :
```json
{
  "username": "user@example.com",
  "password": "yourpassword"
}
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.auth.utils import hash_password, verify_password, create_access_token
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.deps import get_db
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
