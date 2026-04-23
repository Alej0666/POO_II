# -*- coding: utf-8 -*-
"""Rutas de la API para Tareas — Con AsyncSession (E4 integrado)."""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import TareaUpdate
from app.database import get_db
from app.models import Tarea
from src.domain.enums import EstadoTarea

router = APIRouter(prefix="/tareas", tags=["Tareas"])
templates = Jinja2Templates(directory="templates")


@router.patch(
    "/{tarea_id}/completar",
    response_class=HTMLResponse,
    summary="Completar tarea",
)
async def completar_tarea(
    tarea_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    """Marca la tarea como completada. Retorna HTML actualizado (HTMX outerHTML swap)."""
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Cambiar estado a completada
    tarea.estado = EstadoTarea.COMPLETADA
    await session.commit()
    await session.refresh(tarea)
    
    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "tarea_id": tarea.id},
    )


@router.patch(
    "/{tarea_id}/prioridad",
    response_class=HTMLResponse,
    summary="Cambiar prioridad de tarea",
)
async def cambiar_prioridad(
    tarea_id: int,
    request: Request,
    data: TareaUpdate,
    session: AsyncSession = Depends(get_db),
):
    """Cambia la prioridad de la tarea. Retorna HTML actualizado (HTMX outerHTML swap)."""
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if tarea.estado == EstadoTarea.COMPLETADA:
        raise HTTPException(
            status_code=422,
            detail="No se puede cambiar la prioridad de una tarea completada"
        )
    
    # Cambiar prioridad
    tarea.prioridad = data.prioridad
    await session.commit()
    await session.refresh(tarea)
    
    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "tarea_id": tarea.id},
    )
