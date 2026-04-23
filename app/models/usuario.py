# -*- coding: utf-8 -*-
"""Modelo Usuario para SQLAlchemy 2.0."""

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Usuario(Base):
    """Modelo Usuario con relación a Proyectos."""

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    activo: Mapped[bool] = mapped_column(default=True)

    # Relación con Proyectos
    proyectos: Mapped[List["Proyecto"]] = relationship(
        "Proyecto",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, username={self.username!r}, email={self.email!r})"


# Import lazy para evitar circular imports
if False:
    from app.models.proyecto import Proyecto
