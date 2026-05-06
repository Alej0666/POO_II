# -*- coding: utf-8 -*-
"""Rutas de autenticación: register y login."""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from api.schemas.usuario import UsuarioCreate, UsuarioOut, TokenResponse, UsuarioLogin
from api.services.usuario_service import UsuarioService
from api.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UsuarioOut, status_code=201, summary="Registrar nuevo usuario")
async def register(
    data: UsuarioCreate,
    session: AsyncSession = Depends(get_db),
):
    """Registra un nuevo usuario con contraseña hasheada.
    
    Args:
        data: Datos del usuario (username, email, password).
        session: Sesión de base de datos.
        
    Returns:
        Usuario creado (sin contraseña).
        
    Raises:
        HTTPException 400: Si el usuario o email ya existe.
    """
    service = UsuarioService(session)
    
    try:
        usuario = await service.create_usuario(
            username=data.username,
            email=data.email,
            password=data.password,
            nombre_completo=data.nombre_completo,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse, summary="Login y obtener token JWT")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    """Autentica un usuario y retorna un token JWT.
    
    Args:
        form_data: Datos del formulario (username, password).
        session: Sesión de base de datos.
        
    Returns:
        Token JWT con tipo "bearer".
        
    Raises:
        HTTPException 401: Si las credenciales son inválidas.
    """
    service = UsuarioService(session)
    
    # Autenticar usuario
    usuario = await service.authenticate_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token
    access_token = create_access_token(usuario.id)
    return {"access_token": access_token, "token_type": "bearer"}
