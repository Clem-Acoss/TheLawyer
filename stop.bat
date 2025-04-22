
REM Terminer les processus npm et uvicorn en arrière-plan (kill)
echo Arrêt des processus npm et uvicorn...
taskkill /IM "node.exe" /F  REM Tuer le processus npm (node.js)
taskkill /IM "python.exe" /F REM Tuer le processus uvicorn (python)
