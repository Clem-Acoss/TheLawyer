#!/bin/bash

OUTFILE="snapshotenv.txt"
echo "📦 Snapshot de l'environnement - $(date)" > $OUTFILE
echo "==========================================" >> $OUTFILE

log_section() {
    echo -e "\n\n=== [$1 - $(date)] ===" >> $OUTFILE
}

log_section "🔧 Versions des outils"
echo "Node: $(node -v 2>&1)" >> $OUTFILE
echo "npm: $(npm -v 2>&1)" >> $OUTFILE
echo "Python: $(python3 --version 2>&1)" >> $OUTFILE
echo "Vite: $(npx vite --version 2>&1)" >> $OUTFILE
echo "Ollama: $(ollama --version 2>&1)" >> $OUTFILE

log_section "🌍 Variables d’environnement"
printenv >> $OUTFILE 2>> $OUTFILE

log_section "📦 Paquets Node.js installés"
npm ls --depth=0 >> $OUTFILE 2>> $OUTFILE

log_section "🐍 Paquets Python installés (venv)"
pip freeze >> $OUTFILE 2>> $OUTFILE

log_section "🌐 Ports écoutés"
lsof -iTCP -sTCP:LISTEN -n -P >> $OUTFILE 2>> $OUTFILE

log_section "🖥️ Infos système macOS"
system_profiler SPSoftwareDataType SPHardwareDataType >> $OUTFILE 2>> $OUTFILE

log_section "🔧 Configuration Git"
git config --list >> $OUTFILE 2>> $OUTFILE

log_section "📁 package.json"
cat package.json >> $OUTFILE 2>> $OUTFILE

log_section "📁 package-lock.json"
cat package-lock.json >> $OUTFILE 2>> $OUTFILE

echo -e "\n✅ Snapshot completé avec succès à $(date)" >> $OUTFILE