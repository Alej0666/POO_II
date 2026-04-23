# -*- coding: utf-8 -*-
"""Configuración de base de datos con SQLAlchemy 2.0 Async."""

import os
import re
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# URL de la base de datos desde .env o fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./taskflow.db")

# Convertir postgresql: a postgresql+psycopg: para async support
if "postgresql:" in DATABASE_URL:
    DATABASE_URL = re.sub(r"^postgresql:", "postgresql+psycopg:", DATABASE_URL)

# Motor async de SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
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
