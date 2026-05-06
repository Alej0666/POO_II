# -*- coding: utf-8 -*-
"""Schemas Pydantic v2 para Tarea."""

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class PrioridadEnum(str, Enum):
    """Enumeración de prioridades."""

    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class EstadoEnum(str, Enum):
    """Enumeración de estados."""

    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"


class TareaCreate(BaseModel):
    """Schema para crear una nueva tarea."""

    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: str | None = Field(None, max_length=500)
    prioridad: PrioridadEnum = PrioridadEnum.MEDIA


class TareaOut(BaseModel):
    """Schema para devolver datos de tarea."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descripcion: str | None = None
    prioridad: str
    estado: str
    proyecto_id: int


class TareaUpdate(BaseModel):
    """Schema para actualizar datos de tarea."""

    titulo: str | None = Field(None, min_length=3, max_length=100)
    descripcion: str | None = Field(None, max_length=500)
    prioridad: PrioridadEnum | None = None
    estado: EstadoEnum | None = None
