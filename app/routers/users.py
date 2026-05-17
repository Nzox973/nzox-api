# Routes CRUD pour la gestion des utilisateurs
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/users", tags=["👤 Utilisateurs"])


@router.get("/", response_model=List[schemas.UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user)  # Route protégée par JWT
):
    """Liste tous les utilisateurs (authentification requise)."""
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserWithItems)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupère un utilisateur par son ID avec ses items."""
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Supprime un compte utilisateur.
    Seul l'utilisateur lui-même peut supprimer son propre compte.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Action non autorisée")
    crud.delete_user(db, user_id)
