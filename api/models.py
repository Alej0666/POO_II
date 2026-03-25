# -*- coding: utf-8 -*-
"""Modelos Pydantic para request y response de la API TaskFlow."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.domain.enums import PrioridadTarea


class UsuarioCreate(BaseModel):
    """Datos para crear un usuario."""

    username: str = Field(..., min_length=3, max_length=50, description="Identificador único alfanumérico")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    nombre_completo: Optional[str] = Field(None, description="Nombre real del usuario")


class UsuarioResponse(BaseModel):
    """Datos de respuesta de un usuario."""

    id: int
    username: str
    email: str
    activo: bool


class ProyectoCreate(BaseModel):
    """Datos para crear un proyecto."""

    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción opcional")
    lider_id: int = Field(..., description="ID del usuario líder")


class ProyectoResponse(BaseModel):
    """Datos de respuesta de un proyecto."""

    id: int
    nombre: str
    descripcion: Optional[str]
    lider_username: str
    total_tareas: int


class TareaCreate(BaseModel):
    """Datos para crear una tarea dentro de un proyecto."""

    titulo: str = Field(..., min_length=3, max_length=100, description="Título de la tarea")
    prioridad: PrioridadTarea = Field(default=PrioridadTarea.MEDIA, description="Prioridad inicial")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")


class TareaUpdate(BaseModel):
    """Datos para actualizar la prioridad de una tarea."""

    prioridad: PrioridadTarea = Field(..., description="Nueva prioridad")
