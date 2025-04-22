# ⚖️ TheLawyer – Assistant Juridique IA

**TheLawyer** est une application web combinant une interface frontend moderne en **React** et une API backend en **FastAPI**, conçue pour assister les utilisateurs dans l'analyse et la compréhension de documents juridiques grâce à l'Intelligence Artificielle.

---

## 🚀 Fonctionnalités

- 📝 Envoi de questions ou documents juridiques (PDF, texte, etc.)
- 🤖 Analyse automatique avec LLM (modèle de langage)
- 📄 Réponses synthétiques, argumentées et compréhensibles
- 💬 Interface conversationnelle (type chatbot)
- 🗂️ Historique des échanges

---

## 🧰 Technologies utilisées

### 🔙 Backend – FastAPI
- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- Outils IA (OpenAI, HuggingFace, etc.)
- Gestion des fichiers & parsing PDF

### 🔜 Frontend – React
- React + TypeScript
- Vite ou Create React App
- Shadcn/UI pour les composants
- TailwindCSS pour le style
- Axios pour les requêtes API

---

## 🛠️ Lancer le projet en local

### 1. Cloner le dépôt

```bash
git clone https://github.com/Clem-Acoss/TheLawyer.git
cd TheLawyer
uvicorn main:app --reload >>>> dans backend 
npm i  npm run dev >>>> dans droit-ai-interface 