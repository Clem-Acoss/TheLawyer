@echo off

REM Vérifier si les dépendances Python sont installées dans le dossier backend
IF NOT EXIST "backend\venv" (
    echo Aucun environnement virtuel trouvé dans le dossier backend. Création d'un nouvel environnement...
    python -m venv backend\venv
)

echo Activation de l'environnement virtuel backend...
call backend\venv\Scripts\activate

echo Vérification et installation des dépendances Python...
pip install -r backend\requirements.txt

REM Lancer le projet front-end dans une nouvelle fenêtre de commande (en arrière-plan, cachée)
start /B cmd /C "cd droit-ai-interface && npm run dev >nul 2>&1"

REM Vérifier que npm a démarré correctement
echo Vérification que le serveur frontend est en cours d'exécution...
timeout /t 5 /nobreak

REM Ouvrir automatiquement le navigateur à l'URL du front-end
echo Ouverture du navigateur sur http://localhost:8080...
start chrome http://localhost:8080

REM Retour au dossier principal pour lancer le serveur backend
cd backend

REM Lancer le serveur uvicorn dans une nouvelle fenêtre de commande (en arrière-plan, cachée)
start /B cmd /C "uvicorn main:app --reload >nul 2>&1"

REM Laisser la console principale ouverte pour consulter les logs
echo Appuyez sur une touche pour quitter le script...
pause
