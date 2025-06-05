"""
Fichier : config.py
--------------------

Ce module centralise la configuration de l’application backend.

Il utilise `dotenv` pour charger les variables d’environnement définies dans un fichier `.env`.

Paramètres principaux :
- `DATABASE_URL` : URL de connexion à la base de données PostgreSQL
- `SECRET_KEY` : clé secrète utilisée pour la génération et la validation des tokens JWT
- `ALGORITHM` : algorithme utilisé pour signer les tokens JWT (par défaut : HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` : durée de validité des tokens d’accès en minutes

Composants :
- `os` : lecture des variables d’environnement
- `dotenv` : chargement automatique depuis un fichier `.env`

Remarques :
- Si `SECRET_KEY` n’est pas défini dans le fichier `.env`, une valeur par défaut est utilisée
- Ce module est importé dans les parties liées à la sécurité, l’authentification et la base de données
"""


import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
