# Routes d'authentification : inscription, connexion, profil
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud, schemas
from ..auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/auth", tags=["🔐 Authentification"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau compte utilisateur.

    - **email** : adresse email unique
    - **username** : nom d'utilisateur unique
    - **password** : mot de passe (stocké haché avec bcrypt)
    """
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Connexion avec username + password.
    Retourne un token JWT Bearer valable 30 minutes.
    """
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_active_user)):
    """Retourne le profil de l'utilisateur actuellement connecté."""
    return current_user
