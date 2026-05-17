# Opérations CRUD — couche d'accès aux données
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .auth import get_password_hash


# ─────────────────────────────── USERS ───────────────────────────────

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Récupère un utilisateur par son ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Récupère un utilisateur par son email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Récupère un utilisateur par son nom d'utilisateur."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Retourne une liste paginée d'utilisateurs."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Crée un utilisateur avec son mot de passe haché."""
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    """Supprime un utilisateur et retourne l'objet supprimé."""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# ─────────────────────────────── ITEMS ───────────────────────────────

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """Récupère un item par son ID."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """Retourne tous les items publics, paginés."""
    return db.query(models.Item).filter(models.Item.is_public.is_(True)).offset(skip).limit(limit).all()


def get_user_items(db: Session, user_id: int) -> List[models.Item]:
    """Retourne tous les items d'un utilisateur (publics et privés)."""
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()


def create_item(db: Session, item: schemas.ItemCreate, owner_id: int) -> models.Item:
    """Crée un item pour l'utilisateur donné."""
    db_item = models.Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(
    db: Session, item_id: int, item_update: schemas.ItemUpdate, owner_id: int
) -> Optional[models.Item]:
    """Met à jour partiellement un item — seul le propriétaire peut modifier."""
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == owner_id
    ).first()
    if not db_item:
        return None
    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int, owner_id: int) -> Optional[models.Item]:
    """Supprime un item — seul le propriétaire peut supprimer."""
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == owner_id
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
