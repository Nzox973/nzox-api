"""Routes CRUD des items avec contrôle de propriété."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from .. import crud, schemas
from ..dependencies import CurrentUser, DbSession

router = APIRouter(prefix="/items", tags=["📦 Items"])
Skip = Annotated[int, Query(ge=0)]
Limit = Annotated[int, Query(ge=1, le=100)]


@router.get("/", response_model=list[schemas.ItemResponse])
def list_items(db: DbSession, skip: Skip = 0, limit: Limit = 20):
    """Liste seulement les items publics."""
    return crud.get_items(db, skip=skip, limit=limit)


@router.get("/me", response_model=list[schemas.ItemResponse])
def get_my_items(db: DbSession, current_user: CurrentUser):
    """Retourne les items publics et privés de leur propriétaire."""
    return crud.get_user_items(db, current_user.id)


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: DbSession):
    """Récupère un item seulement s'il est public."""
    db_item = crud.get_public_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return db_item


@router.post("/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: DbSession, current_user: CurrentUser):
    """Crée un item pour l'utilisateur connecté."""
    return crud.create_item(db, item, owner_id=current_user.id)


@router.patch("/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    item_update: schemas.ItemUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Modifie un item appartenant à l'utilisateur connecté."""
    db_item = crud.update_item(db, item_id, item_update, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item introuvable ou accès refusé")
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: DbSession, current_user: CurrentUser):
    """Supprime un item appartenant à l'utilisateur connecté."""
    db_item = crud.delete_item(db, item_id, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item introuvable ou accès refusé")
