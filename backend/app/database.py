
"""
Fichier : database.py
---------------------

Ce module configure la connexion à la base de données via SQLAlchemy.

Il inclut :
- La création de l’engine SQLAlchemy à partir de l’URL de connexion
- La configuration du sessionmaker pour gérer les sessions de base de données
- La déclaration de la classe de base ORM `Base` utilisée pour définir les modèles

Fonctionnalités principales :
- `engine` : moteur de connexion à la base de données
- `SessionLocal` : usine à sessions (sessions individuelles pour chaque requête)
- `Base` : classe de base pour les modèles ORM (tables)

Dépendances :
- `DATABASE_URL` importé depuis la configuration de l’application

Remarques :
- Les sessions créées par `SessionLocal` doivent être correctement ouvertes et fermées dans le contexte d’utilisation
- `Base` doit être utilisée pour hériter tous les modèles SQLAlchemy dans l’application
- Le module est central pour l’accès et la manipulation des données persistantes
"""



from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
from app.config import (
    DATABASE_URL,
    DB_NAME,
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)

# --- Base The Lawyer (SQLAlchemy) ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Connexion psycopg2 vers CRA ---
def get_cra_connection():
    db_config = {
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
    return psycopg2.connect(**db_config)