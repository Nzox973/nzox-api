"""Point d'entrée de Nzox API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import settings
from .database import engine
from .routers import auth, items, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialise le schéma au démarrage sans effet de bord à l'import."""
    models.Base.metadata.create_all(bind=engine)
    yield

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
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
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
