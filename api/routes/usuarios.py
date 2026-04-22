# -*- coding: utf-8 -*-
"""Rutas de la API para usuarios."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from api.models import UsuarioCreate, UsuarioResponse
from api.storage import next_usuario_id, usuarios_db
from src.domain.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def _html_lista_usuarios() -> str:
    """Fragmento HTML de la lista de usuarios (li items)."""
    if not usuarios_db:
        return '<li class="list-group-item text-muted small">Sin usuarios aún.</li>'
    return "".join(
        f'<li class="list-group-item d-flex justify-content-between align-items-center small">'
        f'<span><i class="bi bi-person me-1 text-secondary"></i>'
        f'<strong>{u.username}</strong>'
        f'<span class="badge bg-secondary ms-2">ID: {uid}</span></span>'
        f'<span class="text-muted">{u.email}</span></li>'
        for uid, u in usuarios_db.items()
    )


def _html_opciones_usuarios() -> str:
    """Fragmento HTML de <option> para el select de lider."""
    if not usuarios_db:
        return '<option value="" disabled>— Crea un usuario primero —</option>'
    return '<option value="" disabled>— Seleccionar líder —</option>' + "".join(
        f'<option value="{uid}">{u.username} ({u.email})</option>'
        for uid, u in usuarios_db.items()
    )


@router.get("", response_model=list[UsuarioResponse], summary="Listar todos los usuarios")
def listar_usuarios():
    """Retorna la lista de todos los usuarios registrados."""
    return [
        UsuarioResponse(id=uid, username=u.username, email=u.email, activo=u.activo)
        for uid, u in usuarios_db.items()
    ]


@router.get("/opciones", response_class=HTMLResponse, include_in_schema=False)
def opciones_usuarios():
    """Opciones <option> para el select de líder (HTMX)."""
    return HTMLResponse(_html_opciones_usuarios())


@router.post("", status_code=201, summary="Crear usuario")
def crear_usuario(request: Request, data: UsuarioCreate):
    """Crea un nuevo usuario.
    - Desde HTMX (HX-Request): devuelve fragmento HTML con la lista actualizada.
    - Desde Swagger/API: devuelve UsuarioResponse JSON.
    """
    try:
        usuario = Usuario(
            username=data.username,
            email=data.email,
            nombre_completo=data.nombre_completo,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    uid = next_usuario_id()
    usuarios_db[uid] = usuario

    if request.headers.get("HX-Request"):
        # Lista actualizada + OOB swap para el select de líder en el form de proyectos
        oob = f'<select id="select-lider" hx-swap-oob="innerHTML">{_html_opciones_usuarios()}</select>'
        return HTMLResponse(content=_html_lista_usuarios() + oob, status_code=201)

    return UsuarioResponse(id=uid, username=usuario.username, email=usuario.email, activo=usuario.activo)


@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Obtener usuario por ID")
def obtener_usuario(usuario_id: int):
    """Retorna un usuario por su ID. Retorna 404 si no existe."""
    usuario = usuarios_db.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse(id=usuario_id, username=usuario.username, email=usuario.email, activo=usuario.activo)
