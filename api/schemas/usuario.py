# -*- coding: utf-8 -*-
"""Schemas Pydantic v2 para Usuario."""

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UsuarioCreate(BaseModel):
    """Schema para crear un nuevo usuario con contraseña."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    nombre_completo: str | None = None


class UsuarioOut(BaseModel):
    """Schema para devolver datos de usuario (sin contraseña)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    nombre_completo: str | None = None
    activo: bool


class UsuarioUpdate(BaseModel):
    """Schema para actualizar datos de usuario."""

    email: EmailStr | None = None
    nombre_completo: str | None = None
    activo: bool | None = None


class UsuarioLogin(BaseModel):
    """Schema para login con username y password."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Response con JWT token."""

    access_token: str
    token_type: str = "bearer"
