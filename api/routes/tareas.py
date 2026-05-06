# -*- coding: utf-8 -*-
"""Rutas de la API para Tareas — Con AsyncSession + JWT (E5)."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Usuario, Proyecto, Tarea
from api.schemas.tarea import TareaCreate, TareaOut, TareaUpdate
from api.services.tarea_service import TareaService
from api.services.proyecto_service import ProyectoService
from api.auth import get_current_user

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.post("/proyectos/{proyecto_id}/tareas", response_model=TareaOut, status_code=201, summary="Crear tarea")
async def crear_tarea(
    proyecto_id: int,
    data: TareaCreate,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crea una nueva tarea en un proyecto (solo el propietario del proyecto)."""
    # Verificar que el proyecto existe y pertenece al usuario
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear tareas en este proyecto",
        )
    
    service = TareaService(session)
    
    try:
        tarea = await service.create_tarea(
            titulo=data.titulo,
            proyecto_id=proyecto_id,
            prioridad=data.prioridad.value,
            descripcion=data.descripcion,
        )
        return tarea
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/proyectos/{proyecto_id}/tareas", response_model=list[TareaOut], summary="Listar tareas del proyecto")
async def listar_tareas_proyecto(
    proyecto_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtiene todas las tareas de un proyecto (validar propiedad)."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este proyecto",
        )
    
    stmt = select(Tarea).where(Tarea.proyecto_id == proyecto_id).order_by(Tarea.id)
    result = await session.execute(stmt)
    tareas = result.scalars().all()
    return tareas


@router.get("/tareas/{tarea_id}", response_model=TareaOut, summary="Obtener tarea por ID")
async def obtener_tarea(
    tarea_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtiene una tarea específica (validar propiedad del proyecto)."""
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    # Verificar que el usuario es propietario del proyecto
    proyecto = await session.get(Proyecto, tarea.proyecto_id)
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta tarea",
        )
    
    return tarea


@router.put("/tareas/{tarea_id}", response_model=TareaOut, summary="Actualizar tarea")
async def actualizar_tarea(
    tarea_id: int,
    data: TareaUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualiza datos de una tarea (solo el propietario del proyecto)."""
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    # Verificar propiedad
    proyecto = await session.get(Proyecto, tarea.proyecto_id)
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar esta tarea",
        )
    
    service = TareaService(session)
    
    # Preparar campos a actualizar
    update_data = {}
    if data.titulo is not None:
        update_data["titulo"] = data.titulo
    if data.descripcion is not None:
        update_data["descripcion"] = data.descripcion
    if data.prioridad is not None:
        update_data["prioridad"] = data.prioridad.value
    if data.estado is not None:
        update_data["estado"] = data.estado.value
    
    try:
        tarea_actualizada = await service.update_tarea(tarea_id, **update_data)
        return tarea_actualizada
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar tarea")
async def eliminar_tarea(
    tarea_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Elimina una tarea (solo el propietario del proyecto)."""
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    # Verificar propiedad
    proyecto = await session.get(Proyecto, tarea.proyecto_id)
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta tarea",
        )
    
    service = TareaService(session)
    await service.delete_tarea(tarea_id)

