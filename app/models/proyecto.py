# -*- coding: utf-8 -*-
"""Modelo Proyecto para SQLAlchemy 2.0."""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.tarea import Tarea


class Proyecto(Base):
    """Modelo Proyecto con relación a Usuario y Tareas."""

    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="proyectos",
    )
    tareas: Mapped[List["Tarea"]] = relationship(
        "Tarea",
        back_populates="proyecto",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Proyecto(id={self.id}, nombre={self.nombre!r}, usuario_id={self.usuario_id})"
