from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ─────────────────────────────── TOKEN ───────────────────────────────

class Token(BaseModel):
    """Réponse de l'endpoint de connexion."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Données extraites du payload JWT."""
    username: str | None = None


# ─────────────────────────────── USER ────────────────────────────────

class UserCreate(BaseModel):
    """Corps de la requête d'inscription."""

    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_-]+$")
    password: str = Field(min_length=12, max_length=128)


class UserPublic(BaseModel):
    """Profil publiable : aucune adresse email."""

    id: int
    username: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPrivate(UserPublic):
    """Profil retourné uniquement à son propriétaire."""

    email: EmailStr


# ─────────────────────────────── ITEM ────────────────────────────────

class ItemBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1_000)
    is_public: bool = True


class ItemCreate(ItemBase):
    """Corps de la requête de création d'un item."""


class ItemUpdate(BaseModel):
    """Mise à jour partielle — tous les champs sont optionnels."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1_000)
    is_public: bool | None = None


class ItemResponse(ItemBase):
    """Réponse publique d'un item."""
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithPublicItems(UserPublic):
    """Profil public avec seulement les items explicitement publics."""

    items: list[ItemResponse] = Field(default_factory=list)
