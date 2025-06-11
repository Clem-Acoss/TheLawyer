# Étape 1 : Build du frontend (React + Vite)
FROM node:20 AS frontend-builder

WORKDIR /frontend

COPY droit-ai-interface/package*.json ./
RUN npm install

COPY droit-ai-interface/ ./

# Ajout de ARG pour pouvoir passer la variable depuis docker-compose
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

RUN VITE_API_URL=${VITE_API_URL} npm run build


# Étape 2 : Backend (FastAPI) + Copie du frontend compilé
FROM python:3.11-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

# Copier le frontend compilé dans app/static
COPY --from=frontend-builder /frontend/dist ./app/static

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]