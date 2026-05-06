# -*- coding: utf-8 -*-
"""Servicio de negocio para proyectos."""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Proyecto
from api.repositories.proyecto_repo import ProyectoRepository


class ProyectoService:
    """Servicio de negocio para operaciones de proyecto."""

    def __init__(self, session: AsyncSession):
        """Inicializa el servicio con una sesión de BD.
        
        Args:
            session: Sesión async de SQLAlchemy.
        """
        self.repo = ProyectoRepository(session)

    async def create_proyecto(self, nombre: str, usuario_id: int, 
                            descripcion: str | None = None) -> Proyecto:
        """Crea un nuevo proyecto.
        
        Args:
            nombre: Nombre del proyecto (mínimo 3 caracteres).
            usuario_id: ID del usuario propietario.
            descripcion: Descripción opcional.
            
        Returns:
            Proyecto creado.
            
        Raises:
            ValueError: Si el nombre es muy corto.
        """
        if len(nombre) < 3:
            raise ValueError("El nombre del proyecto debe tener al menos 3 caracteres.")
        
        return await self.repo.create_proyecto(nombre, usuario_id, descripcion)

    async def get_proyectos_by_usuario(self, usuario_id: int) -> List[Proyecto]:
        """Obtiene todos los proyectos de un usuario.
        
        Args:
            usuario_id: ID del usuario propietario.
            
        Returns:
            Lista de proyectos del usuario.
        """
        return await self.repo.find_by_usuario_id(usuario_id)

    async def get_proyecto_by_id(self, proyecto_id: int) -> Proyecto | None:
        """Obtiene un proyecto por su ID.
        
        Args:
            proyecto_id: Identificador del proyecto.
            
        Returns:
            Proyecto encontrado o None.
        """
        return await self.repo.get_by_id(proyecto_id)

    async def update_proyecto(self, proyecto_id: int, **kwargs) -> Proyecto | None:
        """Actualiza datos de un proyecto.
        
        Args:
            proyecto_id: ID del proyecto.
            **kwargs: Campos a actualizar (nombre, descripcion).
            
        Returns:
            Proyecto actualizado o None si no existe.
            
        Raises:
            ValueError: Si hay validaciones fallidas.
        """
        # Validar nombre si se está actualizando
        if "nombre" in kwargs and len(kwargs["nombre"]) < 3:
            raise ValueError("El nombre del proyecto debe tener al menos 3 caracteres.")
        
        return await self.repo.update(proyecto_id, **kwargs)

    async def delete_proyecto(self, proyecto_id: int) -> bool:
        """Elimina un proyecto (y sus tareas en cascada).
        
        Args:
            proyecto_id: ID del proyecto a eliminar.
            
        Returns:
            True si se eliminó, False si no existe.
        """
        return await self.repo.delete(proyecto_id)
