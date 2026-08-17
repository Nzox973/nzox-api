"""Configuration centralisée, chargée depuis l'environnement."""

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

_UNSAFE_SECRETS = {
    "dev-only-change-me",
    "changez-cette-cle-secrete-en-production-utilisez-openssl-rand-hex-32",
    "remplacer-par-au-moins-32-caracteres-aleatoires",
}


@dataclass(frozen=True)
class Settings:
    """Paramètres nécessaires au démarrage de l'API."""

    secret_key: str
    database_url: str
    cors_origins: tuple[str, ...]


@lru_cache
def get_settings() -> Settings:
    """Valide les variables d'environnement et retourne une configuration immuable."""
    secret_key = os.getenv("SECRET_KEY", "").strip()
    if len(secret_key) < 32 or secret_key in _UNSAFE_SECRETS:
        raise RuntimeError(
            "SECRET_KEY doit contenir au moins 32 caractères aléatoires. "
            "Consultez .env.example."
        )

    cors_origins = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173",
        ).split(",")
        if origin.strip()
    )
    if "*" in cors_origins:
        raise RuntimeError(
            "CORS_ORIGINS ne peut pas contenir '*' pour cette API authentifiée."
        )

    return Settings(
        secret_key=secret_key,
        database_url=os.getenv("DATABASE_URL", "sqlite:///./nzox_api.db").strip(),
        cors_origins=cors_origins,
    )


settings = get_settings()
