# auth/

Ce dossier contient la logique liée à l'authentification et à la gestion des utilisateurs.

## Contenu typique
- `routes.py` : définit les endpoints liés à l'inscription, la connexion, et la récupération du profil utilisateur.
- `auth_utils.py` : contient les fonctions utilitaires pour le hachage des mots de passe, la génération/validation de JWT, etc.
- `schemas.py` : contient les schémas Pydantic pour les requêtes et les réponses liées à l'authentification.

## Fonctionnalités implémentées
- Création de compte utilisateur
- Connexion par mot de passe
- Authentification via JWT
- Récupération du profil utilisateur connecté

