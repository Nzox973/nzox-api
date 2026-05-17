# Configuration de la base de données SQLite avec SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fichier SQLite local — remplacer par une URL PostgreSQL en production
SQLALCHEMY_DATABASE_URL = "sqlite:///./nzox_api.db"

# check_same_thread=False est obligatoire avec SQLite en contexte multi-thread
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
