# -*- coding: utf-8 -*-
"""Aplicación principal FastAPI — TaskFlow."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import proyectos, tareas, usuarios

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    description="Gestión de proyectos y tareas — Evaluación 3",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    """Página principal de TaskFlow."""
    from api.storage import proyectos_db, usuarios_db
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "proyectos": [{"id": pid, "proyecto": p} for pid, p in proyectos_db.items()],
            "usuarios": [{"id": uid, "usuario": u} for uid, u in usuarios_db.items()],
        },
    )
