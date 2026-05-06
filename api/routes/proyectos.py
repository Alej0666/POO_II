# -*- coding: utf-8 -*-
"""Rutas de la API para Proyectos — Con AsyncSession + JWT (E5)."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Usuario, Proyecto
from api.schemas.proyecto import ProyectoCreate, ProyectoOut, ProyectoUpdate
from api.services.proyecto_service import ProyectoService
from api.auth import get_current_user

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.get("", response_model=list[ProyectoOut], summary="Listar proyectos del usuario autenticado")
async def listar_proyectos(
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Devuelve lista de proyectos del usuario autenticado."""
    stmt = (
        select(Proyecto)
        .where(Proyecto.usuario_id == current_user.id)
        .options(joinedload(Proyecto.tareas))
        .order_by(Proyecto.id)
    )
    result = await session.execute(stmt)
    proyectos = result.unique().scalars().all()
    return proyectos


@router.get("/{proyecto_id}", response_model=ProyectoOut, summary="Obtener proyecto por ID")
async def obtener_proyecto(
    proyecto_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtiene un proyecto específico (validar propiedad)."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    # Validar propiedad
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este proyecto",
        )
    
    return proyecto


@router.post("", response_model=ProyectoOut, status_code=201, summary="Crear proyecto")
async def crear_proyecto(
    data: ProyectoCreate,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crea un nuevo proyecto asociado al usuario autenticado."""
    service = ProyectoService(session)
    
    try:
        proyecto = await service.create_proyecto(
            nombre=data.nombre,
            usuario_id=current_user.id,
            descripcion=data.descripcion,
        )
        return proyecto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{proyecto_id}", response_model=ProyectoOut, summary="Actualizar proyecto")
async def actualizar_proyecto(
    proyecto_id: int,
    data: ProyectoUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualiza datos de un proyecto (solo el propietario)."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    # Validar propiedad
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este proyecto",
        )
    
    service = ProyectoService(session)
    
    # Preparar campos a actualizar
    update_data = {}
    if data.nombre is not None:
        update_data["nombre"] = data.nombre
    if data.descripcion is not None:
        update_data["descripcion"] = data.descripcion
    
    try:
        proyecto_actualizado = await service.update_proyecto(proyecto_id, **update_data)
        return proyecto_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar proyecto")
async def eliminar_proyecto(
    proyecto_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Elimina un proyecto (y sus tareas en cascada)."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    # Validar propiedad
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este proyecto",
        )
    
    service = ProyectoService(session)
    await service.delete_proyecto(proyecto_id)
