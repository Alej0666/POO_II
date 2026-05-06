# -*- coding: utf-8 -*-
"""Repositorio genérico base para patrones CRUD."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Repositorio genérico abstracto para operaciones CRUD básicas.
    
    Proporciona una interfaz estándar para acceso a datos con AsyncSession.
    """

    def __init__(self, session: AsyncSession, model_class: type[T]):
        """Inicializa el repositorio.
        
        Args:
            session: Sesión async de SQLAlchemy.
            model_class: Clase del modelo ORM.
        """
        self.session = session
        self.model_class = model_class

    async def create(self, obj: T) -> T:
        """Crea un nuevo objeto en la base de datos.
        
        Args:
            obj: Objeto a persistir.
            
        Returns:
            Objeto creado con ID asignado.
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        """Obtiene un objeto por su ID.
        
        Args:
            obj_id: Identificador único del objeto.
            
        Returns:
            Objeto encontrado o None.
        """
        return await self.session.get(self.model_class, obj_id)

    async def list_all(self) -> List[T]:
        """Obtiene todos los objetos.
        
        Returns:
            Lista de todos los objetos.
        """
        stmt = select(self.model_class)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, obj_id: int, **kwargs) -> Optional[T]:
        """Actualiza campos específicos de un objeto.
        
        Args:
            obj_id: Identificador del objeto a actualizar.
            **kwargs: Campos a actualizar.
            
        Returns:
            Objeto actualizado o None si no existe.
        """
        obj = await self.get_by_id(obj_id)
        if not obj:
            return None
        
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        """Elimina un objeto por su ID.
        
        Args:
            obj_id: Identificador del objeto a eliminar.
            
        Returns:
            True si se eliminó, False si no existe.
        """
        obj = await self.get_by_id(obj_id)
        if not obj:
            return False
        
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def count(self) -> int:
        """Cuenta el total de objetos.
        
        Returns:
            Total de objetos en la tabla.
        """
        from sqlalchemy import func
        stmt = select(func.count()).select_from(self.model_class)
        result = await self.session.execute(stmt)
        return result.scalar() or 0
