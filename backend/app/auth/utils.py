
"""
Fichier : utils.py (dossier auth)
----------------------------------

Ce module regroupe les fonctions utilitaires liées à l’authentification : 
hachage de mots de passe, vérification, et génération de jetons JWT.

Fonctionnalités :
- hash_password(password) : Retourne un mot de passe haché via bcrypt.
- verify_password(plain, hashed) : Vérifie si un mot de passe brut correspond à un hachage existant.
- create_access_token(data) : Génère un token JWT signé contenant les données fournies
  (généralement l'identifiant de l'utilisateur) avec une date d’expiration.

Dépendances :
- passlib (bcrypt) : Pour le hachage et la vérification sécurisée des mots de passe.
- jose.jwt : Pour la création de tokens JWT.
- config.py : Contient les constantes sensibles (clé secrète, algorithme, durée d’expiration).

Utilisation :
Ces fonctions sont appelées dans les routes d'authentification :
- `hash_password()` lors de l'inscription
- `verify_password()` lors de la connexion
- `create_access_token()` pour renvoyer un token après une authentification réussie

Exemple :
```python
token = create_access_token(data={"sub": str(user.id)})
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
