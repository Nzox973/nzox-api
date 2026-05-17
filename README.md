# 🚀 Nzox API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

API REST complète construite avec **FastAPI**, **SQLAlchemy** et **SQLite**. Authentification JWT, CRUD complet pour les utilisateurs et les items, documentation Swagger automatique.

---

## ✨ Fonctionnalités

| Feature | Détail |
|---|---|
| 🔐 Auth JWT | Inscription, connexion, token Bearer 30 min |
| 👤 Users | CRUD utilisateurs avec hachage bcrypt |
| 📦 Items | CRUD complet avec ownership |
| 📖 Swagger | Docs interactives sur `/docs` |
| 📄 ReDoc | Docs alternatives sur `/redoc` |
| 🛡️ Sécurité | Validation Pydantic, routes protégées |

---

## 📁 Structure du projet

```
nzox-api/
├── app/
│   ├── main.py          # Point d'entrée FastAPI
│   ├── database.py      # Config SQLAlchemy + SQLite
│   ├── models.py        # Modèles ORM
│   ├── schemas.py       # Schémas Pydantic
│   ├── crud.py          # Opérations CRUD
│   ├── auth.py          # JWT + bcrypt
│   ├── dependencies.py  # Dépendances FastAPI
│   └── routers/
│       ├── auth.py      # /auth/*
│       ├── users.py     # /users/*
│       └── items.py     # /items/*
├── requirements.txt
└── README.md
```

---

## ⚡ Démarrage rapide

```bash
# 1. Cloner le repo
git clone https://github.com/Nzox973/nzox-api.git
cd nzox-api

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le serveur
uvicorn app.main:app --reload
```

L'API est disponible sur **http://localhost:8000**
Swagger UI : **http://localhost:8000/docs**

---

## 🔐 Authentification

```bash
# 1. Créer un compte
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "username": "nzox", "password": "secret"}'

# 2. Se connecter (récupérer le token)
curl -X POST http://localhost:8000/auth/login \
  -d "username=nzox&password=secret"

# 3. Utiliser le token
curl -H "Authorization: Bearer <token>" http://localhost:8000/auth/me
```

---

## 📡 Endpoints

### 🔐 Auth
| Méthode | Route | Description |
|---|---|---|
| `POST` | `/auth/register` | Créer un compte |
| `POST` | `/auth/login` | Connexion → token JWT |
| `GET` | `/auth/me` | Profil connecté 🔒 |

### 👤 Users
| Méthode | Route | Description |
|---|---|---|
| `GET` | `/users/` | Lister les users 🔒 |
| `GET` | `/users/{id}` | Détail utilisateur |
| `DELETE` | `/users/{id}` | Supprimer son compte 🔒 |

### 📦 Items
| Méthode | Route | Description |
|---|---|---|
| `GET` | `/items/` | Lister les items publics |
| `GET` | `/items/me` | Mes items 🔒 |
| `GET` | `/items/{id}` | Détail item |
| `POST` | `/items/` | Créer un item 🔒 |
| `PATCH` | `/items/{id}` | Modifier un item 🔒 |
| `DELETE` | `/items/{id}` | Supprimer un item 🔒 |

> 🔒 = Authentification requise

---

## 🛠️ Stack technique

- **[FastAPI](https://fastapi.tiangolo.com)** — framework web async moderne
- **[SQLAlchemy](https://sqlalchemy.org)** — ORM Python
- **[SQLite](https://sqlite.org)** — base de données légère
- **[Pydantic v2](https://docs.pydantic.dev)** — validation des données
- **[python-jose](https://github.com/mpdavis/python-jose)** — JWT
- **[passlib + bcrypt](https://passlib.readthedocs.io)** — hachage des mots de passe

---

## 👤 Auteur

**Nzox973** — [github.com/Nzox973](https://github.com/Nzox973)

*🌴 Building from Guyane, shipping to the world.*
