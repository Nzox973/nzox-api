# Nzox API

[![CI](https://github.com/Nzox973/nzox-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Nzox973/nzox-api/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

API REST de démonstration construite avec FastAPI, SQLAlchemy et SQLite. Le projet montre une authentification JWT, un contrôle de propriété des ressources et une séparation explicite entre données publiques et privées.

## Ce que le projet démontre

- API documentée automatiquement avec OpenAPI, Swagger UI et ReDoc ;
- inscription et connexion OAuth2 Password + JWT ;
- mots de passe hachés avec Argon2 via `pwdlib` ;
- validation des entrées avec Pydantic ;
- routes privées protégées par dépendances FastAPI ;
- accès public limité aux profils et items publiables ;
- CORS restreint aux origines configurées ;
- six tests d'API exécutés en CI, avec contrôle statique Ruff.

Ce dépôt est un projet pédagogique. Une mise en production réelle demanderait notamment des migrations Alembic, une base PostgreSQL, une politique de rotation des secrets, une limitation de débit et une supervision.

## Démarrage local

Prérequis : Python 3.11 ou supérieur.

```bash
git clone https://github.com/Nzox973/nzox-api.git
cd nzox-api
python -m venv .venv
```

Activation de l'environnement :

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

Installation et configuration :

```bash
pip install -r requirements.txt
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Copier la valeur générée dans `SECRET_KEY` du fichier `.env`, puis lancer :

```bash
uvicorn app.main:app --reload
```

- API : `http://localhost:8000`
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`
- Healthcheck : `http://localhost:8000/health`

Sous PowerShell, si `cp` n'est pas disponible :

```powershell
Copy-Item .env.example .env
```

## Variables d'environnement

| Variable | Rôle | Valeur par défaut |
|---|---|---|
| `SECRET_KEY` | Signature des JWT ; 32 caractères aléatoires minimum | aucune, démarrage refusé |
| `DATABASE_URL` | URL SQLAlchemy | `sqlite:///./nzox_api.db` |
| `CORS_ORIGINS` | Origines autorisées, séparées par des virgules | ports locaux 3000 et 5173 |

Le joker `*` n'est pas utilisé pour une API authentifiée. Les secrets faibles ou les exemples connus provoquent volontairement un échec au démarrage.

## Parcours API

### 1. Créer un compte

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","username":"nzox","password":"Strong-password-123!"}'
```

### 2. Obtenir un token

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=nzox&password=Strong-password-123!"
```

### 3. Appeler une route privée

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/auth/me
```

## Endpoints et confidentialité

| Méthode | Route | Accès | Données retournées |
|---|---|---|---|
| `POST` | `/auth/register` | public | profil privé du compte créé |
| `POST` | `/auth/login` | public | token JWT |
| `GET` | `/auth/me` | propriétaire | profil avec email |
| `GET` | `/users/` | authentifié | profils sans email |
| `GET` | `/users/{id}` | public | profil sans email + items publics |
| `DELETE` | `/users/{id}` | propriétaire | suppression de son compte |
| `GET` | `/items/` | public | items publics |
| `GET` | `/items/{id}` | public | item public uniquement |
| `GET` | `/items/me` | propriétaire | tous ses items |
| `POST` | `/items/` | authentifié | création |
| `PATCH` | `/items/{id}` | propriétaire | modification |
| `DELETE` | `/items/{id}` | propriétaire | suppression |

Une ressource privée répond `404` sur les routes publiques afin de ne pas confirmer son existence.

## Tests et qualité

```bash
pip install -r requirements-dev.txt
ruff check app tests
python -m pytest -q
```

La suite vérifie notamment :

- la validation minimale des mots de passe ;
- l'absence d'email dans les réponses publiques ;
- l'invisibilité des items privés ;
- le contrôle de propriété sur modification et suppression ;
- le filtrage CORS ;
- la suppression limitée à son propre compte.

## Structure

```text
app/
├── auth.py          # JWT et Argon2
├── config.py        # variables d'environnement validées
├── crud.py          # accès aux données
├── database.py      # moteur et sessions SQLAlchemy
├── dependencies.py  # DB et utilisateur courant
├── main.py          # application et CORS
├── models.py        # modèles ORM
├── schemas.py       # schémas publics et privés
└── routers/         # auth, users et items
tests/
└── test_api.py
```

## Auteur

**Nzox973** — [github.com/Nzox973](https://github.com/Nzox973)

*Building from Guyane, shipping to the world.*
