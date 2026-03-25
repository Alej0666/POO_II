# -*- coding: utf-8 -*-
"""Rutas de la API para proyectos."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.models import ProyectoCreate, ProyectoResponse, TareaCreate
from api.storage import next_proyecto_id, next_tarea_id, proyectos_db, tareas_db, usuarios_db
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse, summary="Listar proyectos (fragmento HTMX)")
def listar_proyectos(request: Request):
    """Devuelve el fragmento HTML de la lista de proyectos para HTMX."""
    proyectos = [
        {"id": pid, "proyecto": p, "total_tareas": len(p.tareas)}
        for pid, p in proyectos_db.items()
    ]
    return templates.TemplateResponse(
        "proyectos/lista.html",
        {"request": request, "proyectos": proyectos},
    )


@router.post("", response_class=HTMLResponse, status_code=201, summary="Crear proyecto")
def crear_proyecto(request: Request, data: ProyectoCreate):
    """Crea un nuevo proyecto y devuelve la lista de proyectos actualizada."""
    lider = usuarios_db.get(data.lider_id)
    if not lider:
        raise HTTPException(status_code=404, detail="Usuario líder no encontrado")
    try:
        proyecto = Proyecto(nombre=data.nombre, lider=lider, descripcion=data.descripcion)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    pid = next_proyecto_id()
    proyectos_db[pid] = proyecto

    proyectos = [
        {"id": i, "proyecto": p, "total_tareas": len(p.tareas)}
        for i, p in proyectos_db.items()
    ]
    return templates.TemplateResponse(
        "proyectos/lista.html",
        {"request": request, "proyectos": proyectos},
        status_code=201,
    )


@router.get("/{proyecto_id}", response_model=ProyectoResponse, summary="Obtener proyecto por ID")
def obtener_proyecto(proyecto_id: int):
    """Retorna los datos de un proyecto. Retorna 404 si no existe."""
    proyecto = proyectos_db.get(proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return ProyectoResponse(
        id=proyecto_id,
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        lider_username=proyecto.lider.username,
        total_tareas=len(proyecto.tareas),
    )


@router.post(
    "/{proyecto_id}/tareas",
    response_class=HTMLResponse,
    status_code=201,
    summary="Agregar tarea a proyecto",
)
def agregar_tarea(proyecto_id: int, request: Request, data: TareaCreate):
    """Agrega una tarea al proyecto y retorna el fragmento HTML del item de tarea."""
    proyecto = proyectos_db.get(proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    try:
        tarea = Tarea(titulo=data.titulo, prioridad=data.prioridad, descripcion=data.descripcion)
        proyecto.agregar_tarea(tarea)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    tid = next_tarea_id()
    tareas_db[tid] = tarea

    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "tarea_id": tid},
        status_code=201,
    )


@router.get(
    "/{proyecto_id}/tareas",
    response_class=HTMLResponse,
    summary="Listar tareas de un proyecto (fragmento HTMX)",
)
def listar_tareas_proyecto(proyecto_id: int, request: Request):
    """Devuelve el fragmento HTML de las tareas de un proyecto."""
    proyecto = proyectos_db.get(proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Mapear cada tarea del proyecto a su ID en tareas_db
    tareas_con_id = []
    for tid, t in tareas_db.items():
        if t in proyecto.tareas:
            tareas_con_id.append({"tarea_id": tid, "tarea": t})

    return templates.TemplateResponse(
        "tareas/lista.html",
        {"request": request, "tareas": tareas_con_id, "proyecto_id": proyecto_id},
    )
