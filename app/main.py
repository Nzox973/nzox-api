# Point d'entrée de l'application — Nzox API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import auth, users, items

# Création automatique des tables au démarrage
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nzox API",
    description="""
## 🚀 API REST — FastAPI · JWT · SQLAlchemy

### Démarrage rapide
1. Créez un compte → `POST /auth/register`
2. Connectez-vous → `POST /auth/login` (récupérez le token)
3. Cliquez sur **Authorize** → entrez `Bearer <token>`
4. Explorez les routes protégées 🔐
    """,
    version="1.0.0",
    contact={"name": "Nzox973", "url": "https://github.com/Nzox973"},
    license_info={"name": "MIT"},
)

# CORS — autoriser toutes les origines (restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routeurs
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)


@app.get("/", tags=["🏠 Accueil"])
def root():
    """Vérifie que l'API est en ligne et retourne les liens utiles."""
    return {
        "message": "Bienvenue sur Nzox API 🚀",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
    }


@app.get("/health", tags=["🏠 Accueil"])
def health_check():
    """Endpoint de healthcheck pour les systèmes de monitoring."""
    return {"status": "ok"}
