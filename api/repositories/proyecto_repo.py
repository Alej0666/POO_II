# -*- coding: utf-8 -*-
"""Repositorio para operaciones de Proyecto."""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Proyecto
from api.repositories.base import BaseRepository


class ProyectoRepository(BaseRepository[Proyecto]):
    """Repositorio especializado para Proyecto con métodos adicionales."""

    def __init__(self, session: AsyncSession):
        """Inicializa el repositorio de proyectos."""
        super().__init__(session, Proyecto)

    async def find_by_usuario_id(self, usuario_id: int) -> List[Proyecto]:
        """Obtiene todos los proyectos de un usuario.
        
        Args:
            usuario_id: ID del usuario propietario.
            
        Returns:
            Lista de proyectos del usuario.
        """
        stmt = (
            select(Proyecto)
            .where(Proyecto.usuario_id == usuario_id)
            .options(joinedload(Proyecto.tareas))
            .order_by(Proyecto.id)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def create_proyecto(self, nombre: str, usuario_id: int, 
                            descripcion: str | None = None) -> Proyecto:
        """Crea un nuevo proyecto.
        
        Args:
            nombre: Nombre del proyecto.
            usuario_id: ID del usuario propietario.
            descripcion: Descripción opcional.
            
        Returns:
            Proyecto creado.
        """
        proyecto = Proyecto(
            nombre=nombre,
            usuario_id=usuario_id,
            descripcion=descripcion,
        )
        return await self.create(proyecto)
