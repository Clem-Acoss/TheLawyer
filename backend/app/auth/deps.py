



"""
Fichier : deps.py (dossier auth)
---------------------------------

Ce module contient des dépendances utilisées dans le système d'authentification de l'API FastAPI.

Fonctionnalités :
- Fournit une session de base de données (`get_db`) à injecter dans les routes ou services.
- Authentifie l'utilisateur courant via un token JWT (`get_current_user`) pour sécuriser les routes protégées.

Fonctions :
- get_db() : Crée une session SQLAlchemy et la ferme automatiquement après usage.
- get_current_user(token, db) : Décode le JWT reçu via OAuth2, extrait l'ID de l'utilisateur,
  le vérifie en base et retourne l’objet `User` correspondant. Lève une exception HTTP 401 en cas d’échec.

Utilisation :
- Ces fonctions sont généralement appelées avec `Depends()` dans les routes pour obtenir 
  un utilisateur authentifié et une session de base de données active.

Dépendances :
- FastAPI : gestion des dépendances et exceptions HTTP
- OAuth2PasswordBearer : récupération du token JWT depuis les en-têtes Authorization
- jose.jwt : déchiffrement et validation du JWT
- SQLAlchemy : accès aux données utilisateur
- config.py : variables secrètes pour décoder le JWT

Exemple :
```python
@app.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app import models, schemas
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import config as auth_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
