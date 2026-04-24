# -*- coding: utf-8 -*-
"""Aplicación principal FastAPI — TaskFlow."""

from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api.routes import proyectos, tareas, usuarios
from app.database import get_db
from app.models import Proyecto, Usuario

# Obtener rutas base
BASE_DIR = Path(__file__).parent.parent

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    description="Gestión de proyectos y tareas — Evaluación 3+4",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)


@app.get("/", include_in_schema=False)
async def home(request: Request, session: AsyncSession = Depends(get_db)):
    """Página principal de TaskFlow."""
    # Cargar proyectos desde BD con usuario y tareas eager-loaded
    stmt = select(Proyecto).options(
        joinedload(Proyecto.usuario),
        joinedload(Proyecto.tareas)
    ).order_by(Proyecto.id)
    result = await session.execute(stmt)
    proyectos_list = result.unique().scalars().all()
    
    # No acceder a .tareas aquí, solo pasar el proyecto
    proyectos_data = [
        {"id": p.id, "proyecto": p}
        for p in proyectos_list
    ]
    
    # Cargar usuarios para la lista en el sidebar
    stmt_usuarios = select(Usuario).order_by(Usuario.username)
    result_usuarios = await session.execute(stmt_usuarios)
    usuarios_list = result_usuarios.scalars().all()
    
    usuarios_data = [
        {"usuario": u}
        for u in usuarios_list
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "proyectos": proyectos_data,
            "usuarios": usuarios_data,
        },
    )
