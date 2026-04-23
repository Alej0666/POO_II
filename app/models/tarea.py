# -*- coding: utf-8 -*-
"""Modelo Tarea para SQLAlchemy 2.0."""

from typing import TYPE_CHECKING, Optional
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from src.domain.enums import EstadoTarea, PrioridadTarea

if TYPE_CHECKING:
    from app.models.proyecto import Proyecto


class Tarea(Base):
    """Modelo Tarea con relación a Proyecto."""

    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    prioridad: Mapped[PrioridadTarea] = mapped_column(
        Enum(PrioridadTarea),
        default=PrioridadTarea.MEDIA,
        nullable=False,
    )
    estado: Mapped[EstadoTarea] = mapped_column(
        Enum(EstadoTarea),
        default=EstadoTarea.PENDIENTE,
        nullable=False,
    )
    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"), nullable=False)

    # Relación con Proyecto
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="tareas",
    )

    def __repr__(self) -> str:
        return f"Tarea(id={self.id}, titulo={self.titulo!r}, proyecto_id={self.proyecto_id})"
