# -*- coding: utf-8 -*-
"""Configuración de base de datos con SQLAlchemy 2.0."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

# Motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,
)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Clase base para todos los modelos
class Base(DeclarativeBase):
    """Clase base para los modelos SQLAlchemy 2.0."""
    pass


def get_db():
    """Dependency para obtener una sesión de BD en FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
