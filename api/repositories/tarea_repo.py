# -*- coding: utf-8 -*-
"""Repositorio para operaciones de Tarea."""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tarea
from api.repositories.base import BaseRepository


class TareaRepository(BaseRepository[Tarea]):
    """Repositorio especializado para Tarea con métodos adicionales."""

    def __init__(self, session: AsyncSession):
        """Inicializa el repositorio de tareas."""
        super().__init__(session, Tarea)

    async def find_by_proyecto_id(self, proyecto_id: int) -> List[Tarea]:
        """Obtiene todas las tareas de un proyecto.
        
        Args:
            proyecto_id: ID del proyecto propietario.
            
        Returns:
            Lista de tareas del proyecto.
        """
        stmt = (
            select(Tarea)
            .where(Tarea.proyecto_id == proyecto_id)
            .order_by(Tarea.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_tarea(self, titulo: str, proyecto_id: int, 
                          prioridad: str, descripcion: str | None = None) -> Tarea:
        """Crea una nueva tarea.
        
        Args:
            titulo: Título de la tarea.
            proyecto_id: ID del proyecto.
            prioridad: Nivel de prioridad (ALTA/MEDIA/BAJA).
            descripcion: Descripción opcional.
            
        Returns:
            Tarea creada.
        """
        tarea = Tarea(
            titulo=titulo,
            proyecto_id=proyecto_id,
            prioridad=prioridad,
            descripcion=descripcion,
        )
        return await self.create(tarea)
