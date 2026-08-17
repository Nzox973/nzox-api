"""Routes publiques minimales et suppression du compte."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from .. import crud, schemas
from ..dependencies import CurrentUser, DbSession

router = APIRouter(prefix="/users", tags=["👤 Utilisateurs"])
Skip = Annotated[int, Query(ge=0)]
Limit = Annotated[int, Query(ge=1, le=100)]


@router.get("/", response_model=list[schemas.UserPublic])
def list_users(
    db: DbSession,
    _current_user: CurrentUser,
    skip: Skip = 0,
    limit: Limit = 20,
):
    """Liste les profils publics sans exposer les adresses email."""
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserWithPublicItems)
def get_user(user_id: int, db: DbSession):
    """Retourne un profil et seulement ses items publics."""
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")
    return schemas.UserWithPublicItems(
        id=db_user.id,
        username=db_user.username,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        items=crud.get_user_public_items(db, user_id),
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DbSession, current_user: CurrentUser):
    """Supprime uniquement le compte de l'utilisateur connecté."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Action non autorisée")
    crud.delete_user(db, user_id)
