# Routes CRUD pour la gestion des items
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/items", tags=["📦 Items"])


@router.get("/", response_model=List[schemas.ItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Liste tous les items publics — accessible sans authentification."""
    return crud.get_items(db, skip=skip, limit=limit)


@router.get("/me", response_model=List[schemas.ItemResponse])
def get_my_items(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Retourne tous les items (publics et privés) de l'utilisateur connecté."""
    return crud.get_user_items(db, current_user.id)


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Récupère un item par son ID."""
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return db_item


@router.post("/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Crée un nouvel item pour l'utilisateur connecté.

    - **title** : titre obligatoire
    - **description** : description optionnelle
    - **is_public** : visible publiquement (défaut : true)
    """
    return crud.create_item(db, item, owner_id=current_user.id)


@router.patch("/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    item_update: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Met à jour partiellement un item existant.
    Seul le propriétaire peut modifier l'item.
    """
    db_item = crud.update_item(db, item_id, item_update, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item introuvable ou accès refusé")
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Supprime un item.
    Seul le propriétaire peut supprimer l'item.
    """
    db_item = crud.delete_item(db, item_id, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item introuvable ou accès refusé")
