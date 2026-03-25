# -*- coding: utf-8 -*-
"""Rutas de la API para tareas."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.models import TareaUpdate
from api.storage import tareas_db
from src.domain.enums import EstadoTarea

router = APIRouter(prefix="/tareas", tags=["Tareas"])
templates = Jinja2Templates(directory="templates")


@router.patch("/{tarea_id}/completar", response_class=HTMLResponse, summary="Completar tarea")
def completar_tarea(tarea_id: int, request: Request):
    """Marca la tarea como completada. Retorna el fragmento HTML actualizado (HTMX outerHTML swap)."""
    tarea = tareas_db.get(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    try:
        tarea.completar()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "tarea_id": tarea_id},
    )


@router.patch("/{tarea_id}/prioridad", response_class=HTMLResponse, summary="Cambiar prioridad de tarea")
def cambiar_prioridad(tarea_id: int, request: Request, data: TareaUpdate):
    """Cambia la prioridad de la tarea. Retorna el fragmento HTML actualizado (HTMX outerHTML swap)."""
    tarea = tareas_db.get(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if tarea.estado == EstadoTarea.COMPLETADA:
        raise HTTPException(status_code=422, detail="No se puede cambiar la prioridad de una tarea completada")
    try:
        tarea.cambiar_prioridad(data.prioridad)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "tarea_id": tarea_id},
    )
