# -*- coding: utf-8 -*-
"""Schemas Pydantic v2 para Proyecto."""

from pydantic import BaseModel, ConfigDict, Field


class ProyectoCreate(BaseModel):
    """Schema para crear un nuevo proyecto."""

    nombre: str = Field(..., min_length=3, max_length=50)
    descripcion: str | None = Field(None, max_length=500)


class ProyectoOut(BaseModel):
    """Schema para devolver datos de proyecto."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None = None
    usuario_id: int


class ProyectoUpdate(BaseModel):
    """Schema para actualizar datos de proyecto."""

    nombre: str | None = Field(None, min_length=3, max_length=50)
    descripcion: str | None = Field(None, max_length=500)
