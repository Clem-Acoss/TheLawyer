# Étape 1 : Build du frontend (React + Vite)
FROM node:20 AS frontend-builder

WORKDIR /frontend
# Copier le reste du code frontend (après installation des dépendances pour cache optimisé)
COPY droit-ai-interface/ ./

RUN npm config set registry http://nexus.urssaf.recouv/repository/npm-proxy/
# Installer les dépendances Node avec logs détaillés
RUN npm install --force --verbose



# Définir l'URL API et build le frontend
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
RUN VITE_API_URL=${VITE_API_URL} npx vite build



# Étape 2 : Backend (FastAPI) + Copie du frontend compilé
FROM ubuntu:22.04 AS backend

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Remplacer les sources APT par le proxy Nexus
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://nexus.urssaf.recouv/repository/apt-proxy/ jammy main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb http://nexus.urssaf.recouv/repository/apt-proxy/ jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://nexus.urssaf.recouv/repository/apt-proxy/ jammy-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://nexus.urssaf.recouv/repository/apt-security/ jammy-security main restricted universe multiverse" >> /etc/apt/sources.list

# Installer Python et dépendances système
RUN apt-get update && \
    apt-get install -y \
        python3.10 \
        python3.10-venv \
        python3-pip \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        poppler-utils \
        python3-pil \
        tesseract-ocr \
        libtesseract-dev \
        tesseract-ocr-eng \
        tesseract-ocr-fra \
        tesseract-ocr-script-latn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurer pip pour Nexus
RUN mkdir -p /etc/pip && \
    echo "[global]" > /etc/pip/pip.conf && \
    echo "index-url = http://nexus.urssaf.recouv/repository/pypi-proxy/simple" >> /etc/pip/pip.conf

WORKDIR /app

# Installer les dépendances Python
COPY backend/requirements.txt .
RUN pip install -v \
    --trusted-host nexus.urssaf.recouv \
    --index-url http://nexus.urssaf.recouv/repository/pypi-proxy/simple/ \
    --timeout 100000 \
    -r requirements.txt

# Copier le code backend
COPY backend/app ./app
COPY backend/app/boss/ /app/boss/
# Copier le frontend compilé dans static
COPY --from=frontend-builder /frontend/dist ./app/static

EXPOSE 8000

# Commande de lancement FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
