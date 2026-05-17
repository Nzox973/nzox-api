# Schémas Pydantic — validation des entrées et sérialisation des réponses
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# ─────────────────────────────── TOKEN ───────────────────────────────

class Token(BaseModel):
    """Réponse de l'endpoint de connexion."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Données extraites du payload JWT."""
    username: Optional[str] = None


# ─────────────────────────────── USER ────────────────────────────────

class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Corps de la requête d'inscription."""
    password: str


class UserResponse(UserBase):
    """Réponse publique — ne contient jamais le mot de passe."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserWithItems(UserResponse):
    """Profil utilisateur avec la liste de ses items."""
    items: List["ItemResponse"] = []


# ─────────────────────────────── ITEM ────────────────────────────────

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True


class ItemCreate(ItemBase):
    """Corps de la requête de création d'un item."""
    pass


class ItemUpdate(BaseModel):
    """Mise à jour partielle — tous les champs sont optionnels."""
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class ItemResponse(ItemBase):
    """Réponse publique d'un item."""
    id: int
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
