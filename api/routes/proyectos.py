# -*- coding: utf-8 -*-
"""Rutas de la API para Proyectos — Con AsyncSession (E4 integrado)."""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import ProyectoCreate, ProyectoResponse, TareaCreate
from app.database import get_db
from app.models import Usuario, Proyecto, Tarea

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse, summary="Listar proyectos (fragmento HTMX)")
async def listar_proyectos(request: Request, session: AsyncSession = Depends(get_db)):
    """Devuelve el fragmento HTML de la lista de proyectos para HTMX."""
    stmt = select(Proyecto).order_by(Proyecto.id)
    result = await session.execute(stmt)
    proyectos_list = result.scalars().all()
    
    proyectos = [
        {"id": p.id, "proyecto": p, "total_tareas": len(p.tareas)}
        for p in proyectos_list
    ]
    return templates.TemplateResponse(
        request=request,
        name="proyectos/lista.html",
        context={"proyectos": proyectos},
    )


@router.post("", response_class=HTMLResponse, status_code=201, summary="Crear proyecto")
async def crear_proyecto(
    request: Request,
    data: ProyectoCreate,
    session: AsyncSession = Depends(get_db),
):
    """Crea un nuevo proyecto en BD y devuelve lista actualizada."""
    # Verificar que el líder existe
    lider = await session.get(Usuario, data.lider_id)
    if not lider:
        raise HTTPException(status_code=404, detail="Usuario líder no encontrado")
    
    # Crear proyecto
    proyecto = Proyecto(nombre=data.nombre, descripcion=data.descripcion, usuario_id=data.lider_id)
    session.add(proyecto)
    await session.commit()
    await session.refresh(proyecto)
    
    # Retornar lista actualizada
    stmt = select(Proyecto).order_by(Proyecto.id)
    result = await session.execute(stmt)
    proyectos_list = result.scalars().all()
    
    proyectos = [
        {"id": p.id, "proyecto": p, "total_tareas": len(p.tareas)}
        for p in proyectos_list
    ]
    return templates.TemplateResponse(
        request=request,
        name="proyectos/lista.html",
        context={"proyectos": proyectos},
        status_code=201,
    )


@router.get("/{proyecto_id}", response_model=ProyectoResponse, summary="Obtener proyecto")
async def obtener_proyecto(
    proyecto_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Retorna datos de un proyecto."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Cargar relación usuario
    await session.refresh(proyecto, ["usuario"])
    
    return ProyectoResponse(
        id=proyecto.id,
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        lider_username=proyecto.usuario.username,
        total_tareas=len(proyecto.tareas),
    )


@router.post(
    "/{proyecto_id}/tareas",
    response_class=HTMLResponse,
    status_code=201,
    summary="Agregar tarea a proyecto",
)
async def agregar_tarea(
    proyecto_id: int,
    request: Request,
    data: TareaCreate,
    session: AsyncSession = Depends(get_db),
):
    """Agrega una tarea al proyecto y retorna el fragmento HTML."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Crear tarea
    tarea = Tarea(
        titulo=data.titulo,
        descripcion=data.descripcion,
        prioridad=data.prioridad,
        proyecto_id=proyecto_id,
    )
    session.add(tarea)
    await session.commit()
    await session.refresh(tarea)
    
    return templates.TemplateResponse(
        request=request,
        name="tareas/item.html",
        context={"tarea": tarea, "tarea_id": tarea.id},
        status_code=201,
    )


@router.get(
    "/{proyecto_id}/tareas",
    response_class=HTMLResponse,
    summary="Listar tareas de un proyecto (fragmento HTMX)",
)
async def listar_tareas_proyecto(
    proyecto_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    """Devuelve el fragmento HTML de las tareas de un proyecto."""
    proyecto = await session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Las tareas están en proyecto.tareas (relación)
    stmt = select(Tarea).where(Tarea.proyecto_id == proyecto_id).order_by(Tarea.id)
    result = await session.execute(stmt)
    tareas_list = result.scalars().all()
    
    tareas_con_id = [{"tarea_id": t.id, "tarea": t} for t in tareas_list]
    
    return templates.TemplateResponse(
        request=request,
        name="tareas/lista.html",
        context={"tareas": tareas_con_id, "proyecto_id": proyecto_id},
    )
