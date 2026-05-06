# -*- coding: utf-8 -*-
"""Repositorio para operaciones de Usuario."""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Usuario
from api.repositories.base import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """Repositorio especializado para Usuario con métodos adicionales."""

    def __init__(self, session: AsyncSession):
        """Inicializa el repositorio de usuarios."""
        super().__init__(session, Usuario)

    async def find_by_username(self, username: str) -> Optional[Usuario]:
        """Busca un usuario por username.
        
        Args:
            username: Nombre de usuario único.
            
        Returns:
            Usuario encontrado o None.
        """
        stmt = select(Usuario).where(Usuario.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por email.
        
        Args:
            email: Correo electrónico único.
            
        Returns:
            Usuario encontrado o None.
        """
        stmt = select(Usuario).where(Usuario.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_usuario(self, username: str, email: str, hashed_password: str, 
                            nombre_completo: Optional[str] = None) -> Usuario:
        """Crea un nuevo usuario con contraseña hasheada.
        
        Args:
            username: Nombre de usuario único.
            email: Correo electrónico único.
            hashed_password: Contraseña hasheada.
            nombre_completo: Nombre completo (opcional).
            
        Returns:
            Usuario creado.
        """
        usuario = Usuario(
            username=username,
            email=email,
            hashed_password=hashed_password,
            nombre_completo=nombre_completo,
            activo=True,
        )
        return await self.create(usuario)
