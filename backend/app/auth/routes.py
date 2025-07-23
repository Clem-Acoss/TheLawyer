
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
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.auth.utils import hash_password, verify_password, create_access_token
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.deps import get_db
from fastapi import BackgroundTasks
from app.auth.email_service import send_email
from app.auth.utils import decode_access_token
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

@router.post("/password-reset/request")
def request_password_reset(payload: schemas.PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token(data={"sub": str(user.id)}, expires_delta=int(os.getenv("JWT_EXP_DELTA_SECONDS", 3600)))

    reset_link = f"{os.getenv('FRONTEND_URL')}/password/reset?token={token}"
    print(f"[PASSWORD RESET] le lien devrait etre en dessous")
    print(f"[PASSWORD RESET] Reset link for {payload.email}: {reset_link}")

    html_content = f"""
    <p>Bonjour,</p>
    <p>Pour réinitialiser votre mot de passe, cliquez sur le lien ci-dessous :</p>
    <p><a href="{reset_link}">Réinitialiser mon mot de passe</a></p>
    <p>Ce lien est valide pour 1 heure.</p>
    """

    background_tasks.add_task(send_email, to_email=payload.email, subject="Réinitialisation de mot de passe", html_content=html_content)
    return {"message": "Un email de réinitialisation a été envoyé."}


@router.post("/password-reset/confirm")
def confirm_password_reset(data: schemas.PasswordResetConfirm, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(data.token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")

    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    new_hashed = hash_password(data.new_password)
    crud.update_user_password(db, user_id=user.id, new_hashed_password=new_hashed)
    return {"message": "Mot de passe mis à jour avec succès."}