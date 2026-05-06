# -*- coding: utf-8 -*-
"""Configuración de autenticación JWT y dependencias de seguridad."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Usuario
from api.repositories.usuario_repo import UsuarioRepository

# Configuración JWT
SECRET_KEY = "tu-clave-secreta-super-segura-en-produccion-usa-env"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT para un usuario.
    
    Args:
        user_id: Identificador del usuario.
        expires_delta: Duración del token (si no se especifica, usa el default).
        
    Returns:
        Token JWT codificado.
    """
    to_encode = {"sub": str(user_id)}
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> Usuario:
    """Decodifica el JWT y retorna el usuario autenticado.
    
    Args:
        token: Token JWT del header Authorization.
        session: Sesión de base de datos.
        
    Returns:
        Usuario autenticado.
        
    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Obtener usuario de la BD
    repo = UsuarioRepository(session)
    user = await repo.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    
    return user
