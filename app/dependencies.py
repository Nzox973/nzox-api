"""Dépendances FastAPI réutilisables."""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import crud, models
from .auth import decode_token
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Generator[Session, None, None]:
    """Ouvre une session SQLAlchemy et la ferme après la requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
TokenString = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: TokenString, db: DbSession) -> models.User:
    """Retourne l'utilisateur du token ou lève une erreur 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


AuthenticatedUser = Annotated[models.User, Depends(get_current_user)]


def get_current_active_user(current_user: AuthenticatedUser) -> models.User:
    """Refuse les comptes désactivés."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte désactivé",
        )
    return current_user


CurrentUser = Annotated[models.User, Depends(get_current_active_user)]
