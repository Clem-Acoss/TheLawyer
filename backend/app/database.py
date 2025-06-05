
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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
