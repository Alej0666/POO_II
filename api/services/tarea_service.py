# -*- coding: utf-8 -*-
"""Servicio de negocio para tareas."""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tarea
from api.repositories.tarea_repo import TareaRepository


class TareaService:
    """Servicio de negocio para operaciones de tarea."""

    def __init__(self, session: AsyncSession):
        """Inicializa el servicio con una sesión de BD.
        
        Args:
            session: Sesión async de SQLAlchemy.
        """
        self.repo = TareaRepository(session)

    async def create_tarea(self, titulo: str, proyecto_id: int, 
                          prioridad: str = "MEDIA", 
                          descripcion: str | None = None) -> Tarea:
        """Crea una nueva tarea.
        
        Args:
            titulo: Título de la tarea (mínimo 3 caracteres).
            proyecto_id: ID del proyecto propietario.
            prioridad: Nivel de prioridad (ALTA/MEDIA/BAJA).
            descripcion: Descripción opcional.
            
        Returns:
            Tarea creada.
            
        Raises:
            ValueError: Si hay validaciones fallidas.
        """
        if len(titulo) < 3:
            raise ValueError("El título de la tarea debe tener al menos 3 caracteres.")
        
        if prioridad not in ["ALTA", "MEDIA", "BAJA"]:
            raise ValueError(f"Prioridad inválida: {prioridad}")
        
        return await self.repo.create_tarea(titulo, proyecto_id, prioridad, descripcion)

    async def get_tareas_by_proyecto(self, proyecto_id: int) -> List[Tarea]:
        """Obtiene todas las tareas de un proyecto.
        
        Args:
            proyecto_id: ID del proyecto.
            
        Returns:
            Lista de tareas del proyecto.
        """
        return await self.repo.find_by_proyecto_id(proyecto_id)

    async def get_tarea_by_id(self, tarea_id: int) -> Tarea | None:
        """Obtiene una tarea por su ID.
        
        Args:
            tarea_id: Identificador de la tarea.
            
        Returns:
            Tarea encontrada o None.
        """
        return await self.repo.get_by_id(tarea_id)

    async def update_tarea(self, tarea_id: int, **kwargs) -> Tarea | None:
        """Actualiza datos de una tarea.
        
        Args:
            tarea_id: ID de la tarea.
            **kwargs: Campos a actualizar (titulo, descripcion, prioridad, estado).
            
        Returns:
            Tarea actualizada o None si no existe.
            
        Raises:
            ValueError: Si hay validaciones fallidas.
        """
        # Validar título si se está actualizando
        if "titulo" in kwargs and len(kwargs["titulo"]) < 3:
            raise ValueError("El título de la tarea debe tener al menos 3 caracteres.")
        
        # Validar prioridad si se está actualizando
        if "prioridad" in kwargs and kwargs["prioridad"] not in ["ALTA", "MEDIA", "BAJA"]:
            raise ValueError(f"Prioridad inválida: {kwargs['prioridad']}")
        
        # Validar estado si se está actualizando
        if "estado" in kwargs and kwargs["estado"] not in ["PENDIENTE", "EN_PROGRESO", "COMPLETADA"]:
            raise ValueError(f"Estado inválido: {kwargs['estado']}")
        
        return await self.repo.update(tarea_id, **kwargs)

    async def delete_tarea(self, tarea_id: int) -> bool:
        """Elimina una tarea.
        
        Args:
            tarea_id: ID de la tarea a eliminar.
            
        Returns:
            True si se eliminó, False si no existe.
        """
        return await self.repo.delete(tarea_id)
