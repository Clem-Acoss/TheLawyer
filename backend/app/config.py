"""
Fichier : config.py
--------------------

Ce module centralise la configuration de l’application backend.

Il utilise `dotenv` pour charger les variables d’environnement définies dans un fichier `.env`.

Paramètres principaux :
- `DATABASE_URL` : URL de connexion à la base de données PostgreSQL (TheLawyer)
- `DB_NAME`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` : connexion à la base CRA via psycopg2
- `SECRET_KEY` : clé secrète utilisée pour JWT
- `ALGORITHM` : algorithme JWT (par défaut : HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` : durée de validité des tokens d’accès en minutes
- Variables pour API embedding, LLM, SMTP, chemins locaux, frontend, etc.

Remarques :
- Si une variable n’est pas définie dans `.env`, une valeur par défaut est utilisée quand c’est pertinent.
- Ce module est importé dans les parties liées à la sécurité, l’authentification, la base de données et les services externes.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Base TheLawyer (SQLAlchemy)
DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://clementgardair:root@db:5432/baseTheLawyer")

# Base CRA (connexion psycopg2)
DB_NAME: str = os.getenv("DB_NAME", "cra")
DB_HOST: str = os.getenv("DB_HOST", "10.207.177.26")
DB_USER: str = os.getenv("DB_USER", "cra")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "rDjZ]Jiat7a*ko)a0Ld7XF^e")
DB_PORT: int = int(os.getenv("DB_PORT", 5432))

# JWT
SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXP_DELTA_SECONDS", 3600))

# API Embedding
EMBEDDING_API_URL: str = os.getenv("EMBEDDING_API_URL", "https://embeddings.urssaf.cloud-acoss.fr/embed")
EMBEDDING_API_TOKEN: str = os.getenv("EMBEDDING_API_TOKEN", "")

# API LLM
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
LLM_API_URL: str = os.getenv("LLM_API_URL", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "")



# SMTP
SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.km.recouv")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", 25))
SMTP_USER: str = os.getenv("SMTP_USER", "")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM: str = os.getenv("SMTP_FROM", "cra-montreuil@acoss.fr")

# Frontend
FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:8000")
