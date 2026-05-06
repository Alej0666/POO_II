# -*- coding: utf-8 -*-
"""Servicio de negocio para usuarios."""

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Usuario
from api.repositories.usuario_repo import UsuarioRepository

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UsuarioService:
    """Servicio de negocio para operaciones de usuario."""

    def __init__(self, session: AsyncSession):
        """Inicializa el servicio con una sesión de BD.
        
        Args:
            session: Sesión async de SQLAlchemy.
        """
        self.repo = UsuarioRepository(session)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashea una contraseña usando bcrypt.
        
        Args:
            password: Contraseña en texto plano.
            
        Returns:
            Contraseña hasheada.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash.
        
        Args:
            plain_password: Contraseña en texto plano.
            hashed_password: Contraseña hasheada almacenada.
            
        Returns:
            True si coinciden, False en caso contrario.
        """
        return pwd_context.verify(plain_password, hashed_password)

    async def create_usuario(self, username: str, email: str, password: str, 
                            nombre_completo: str | None = None) -> Usuario:
        """Crea un nuevo usuario con contraseña hasheada.
        
        Args:
            username: Nombre de usuario único.
            email: Correo electrónico único.
            password: Contraseña en texto plano.
            nombre_completo: Nombre completo (opcional).
            
        Returns:
            Usuario creado.
            
        Raises:
            ValueError: Si el usuario o email ya existe.
        """
        # Verificar que username y email sean únicos
        existing_user = await self.repo.find_by_username(username)
        if existing_user:
            raise ValueError(f"El usuario '{username}' ya existe.")
        
        existing_email = await self.repo.find_by_email(email)
        if existing_email:
            raise ValueError(f"El email '{email}' ya está registrado.")
        
        # Hashear y crear usuario
        hashed_pwd = self.hash_password(password)
        return await self.repo.create_usuario(
            username=username,
            email=email,
            hashed_password=hashed_pwd,
            nombre_completo=nombre_completo,
        )

    async def authenticate_usuario(self, username: str, password: str) -> Usuario | None:
        """Autentica un usuario con username y password.
        
        Args:
            username: Nombre de usuario.
            password: Contraseña en texto plano.
            
        Returns:
            Usuario si la autenticación es exitosa, None en caso contrario.
        """
        user = await self.repo.find_by_username(username)
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        return user

    async def get_usuario_by_id(self, usuario_id: int) -> Usuario | None:
        """Obtiene un usuario por su ID.
        
        Args:
            usuario_id: Identificador del usuario.
            
        Returns:
            Usuario encontrado o None.
        """
        return await self.repo.get_by_id(usuario_id)
