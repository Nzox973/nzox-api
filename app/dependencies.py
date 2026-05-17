# Dépendances FastAPI réutilisables — session DB et authentification
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from .auth import decode_token
from . import crud, models

# Pointe vers l'endpoint de connexion pour le flux OAuth2 dans Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    """Générateur de session DB — ferme automatiquement après chaque requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """Extrait l'utilisateur depuis le token JWT — lève 401 si invalide."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Vérifie que l'utilisateur connecté est bien actif."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte désactivé"
        )
    return current_user
