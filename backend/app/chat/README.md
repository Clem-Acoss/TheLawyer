# chat/

Ce dossier gère la logique métier associée aux conversations entre l'utilisateur et l'assistant IA.

## Contenu typique
- `routes.py` : endpoints pour envoyer un message, récupérer les conversations d'un utilisateur, etc.
- `chat_service.py` : service de traitement des messages, envoi au LLM, sauvegarde des messages, création de threads.
- `schemas.py` : schémas Pydantic pour les messages, conversations et réponses.

## Fonctionnalités implémentées
- Envoi et réception de messages
- Création automatique de threads de conversation
- Historique des échanges par utilisateur
