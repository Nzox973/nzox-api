"""Routes d'inscription, de connexion et de profil privé."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .. import crud, schemas
from ..auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password
from ..dependencies import CurrentUser, DbSession

router = APIRouter(prefix="/auth", tags=["🔐 Authentification"])
LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post(
    "/register",
    response_model=schemas.UserPrivate,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate, db: DbSession):
    """Crée un compte et ne retourne jamais le mot de passe ou son hash."""
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email déjà utilisé")
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=409, detail="Nom d'utilisateur déjà pris")
    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(form_data: LoginForm, db: DbSession):
    """Retourne un token JWT Bearer valable 30 minutes."""
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserPrivate)
def get_me(current_user: CurrentUser):
    """Retourne le profil privé de l'utilisateur connecté."""
    return current_user
