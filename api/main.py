# -*- coding: utf-8 -*-
"""Aplicación principal FastAPI — TaskFlow."""

from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.routes import proyectos, tareas, usuarios
from app.database import get_db
from app.models import Proyecto

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
    # Cargar proyectos desde BD
    stmt = select(Proyecto).order_by(Proyecto.id)
    result = await session.execute(stmt)
    proyectos_list = result.scalars().all()
    
    proyectos_data = [
        {"id": p.id, "proyecto": p, "total_tareas": len(p.tareas)}
        for p in proyectos_list
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "proyectos": proyectos_data,
        },
    )
