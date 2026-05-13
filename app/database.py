# -*- coding: utf-8 -*-
"""Configuración de base de datos con SQLAlchemy 2.0 Async."""

import os
import re
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# URL de la base de datos desde .env o fallback a SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./taskflow.db")

# Convertir postgresql: a postgresql+psycopg: para async support
if "postgresql:" in DATABASE_URL:
    DATABASE_URL = re.sub(r"^postgresql:", "postgresql+psycopg:", DATABASE_URL)
    logger.info("📊 Base de datos: PostgreSQL (async)")
else:
    logger.info("📊 Base de datos: SQLite (desarrollo local)")

# Configurar opciones según el tipo de BD
engine_kwargs = {
    "echo": False,
    "pool_pre_ping": True,
}

# Para SQLite, deshabilitar el pool (no es necesario)
if "sqlite" in DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

# Motor async de SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    **engine_kwargs
)

# Session factory async
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Clase base para modelos SQLAlchemy 2.0."""
    pass


async def get_db():
    """Async dependency: inyecta AsyncSession en rutas."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
