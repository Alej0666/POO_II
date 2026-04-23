# -*- coding: utf-8 -*-
"""Rutas de la API para Usuarios — Con AsyncSession (E4 integrado)."""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UsuarioCreate, UsuarioResponse
from app.database import get_db
from app.models import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


async def _get_usuarios_html(session: AsyncSession) -> str:
    """Genera HTML de lista de usuarios desde BD."""
    stmt = select(Usuario).order_by(Usuario.id)
    result = await session.execute(stmt)
    usuarios = result.scalars().all()
    
    if not usuarios:
        return '<li class="list-group-item text-muted small">Sin usuarios aún.</li>'
    
    return "".join(
        f'<li class="list-group-item d-flex justify-content-between align-items-center small">'
        f'<span><i class="bi bi-person me-1 text-secondary"></i>'
        f'<strong>{u.username}</strong>'
        f'<span class="badge bg-secondary ms-2">ID: {u.id}</span></span>'
        f'<span class="text-muted">{u.email}</span></li>'
        for u in usuarios
    )


async def _get_opciones_usuarios(session: AsyncSession) -> str:
    """Genera <option> tags desde BD para select de líder."""
    stmt = select(Usuario).order_by(Usuario.username)
    result = await session.execute(stmt)
    usuarios = result.scalars().all()
    
    if not usuarios:
        return '<option value="" disabled>— Crea un usuario primero —</option>'
    
    options = '<option value="" disabled>— Seleccionar líder —</option>'
    options += "".join(
        f'<option value="{u.id}">{u.username} ({u.email})</option>'
        for u in usuarios
    )
    return options


@router.get("", response_model=list[UsuarioResponse], summary="Listar usuarios")
async def listar_usuarios(session: AsyncSession = Depends(get_db)):
    """Retorna lista de usuarios desde BD."""
    stmt = select(Usuario).order_by(Usuario.id)
    result = await session.execute(stmt)
    usuarios = result.scalars().all()
    
    return [
        UsuarioResponse(id=u.id, username=u.username, email=u.email, activo=u.activo)
        for u in usuarios
    ]


@router.get("/opciones", response_class=HTMLResponse, include_in_schema=False)
async def opciones_usuarios(session: AsyncSession = Depends(get_db)):
    """Opciones <option> para select de líder (HTMX)."""
    return HTMLResponse(await _get_opciones_usuarios(session))


@router.post("", status_code=201, summary="Crear usuario")
async def crear_usuario(
    request: Request,
    data: UsuarioCreate,
    session: AsyncSession = Depends(get_db),
):
    """Crea usuario en BD.
    - HTMX: devuelve HTML con lista actualizada + OOB swap
    - API: devuelve JSON
    """
    # Verificar que username y email no existan
    stmt = select(Usuario).where(Usuario.username == data.username)
    existing = await session.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=422, detail="Username ya existe")
    
    stmt = select(Usuario).where(Usuario.email == data.email)
    existing = await session.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=422, detail="Email ya existe")
    
    # Crear usuario
    usuario = Usuario(username=data.username, email=data.email, activo=True)
    session.add(usuario)
    await session.flush()  # Para obtener el ID sin commit completo
    uid = usuario.id
    await session.commit()
    await session.refresh(usuario)  # Refresca el objeto
    
    if request.headers.get("HX-Request"):
        lista_html = await _get_usuarios_html(session)
        opciones_html = await _get_opciones_usuarios(session)
        oob = f'<select id="select-lider" hx-swap-oob="innerHTML">{opciones_html}</select>'
        return HTMLResponse(content=lista_html + oob, status_code=201)
    
    return UsuarioResponse(id=uid, username=usuario.username, email=usuario.email, activo=usuario.activo)


@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Obtener usuario")
async def obtener_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Obtiene un usuario por ID."""
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return UsuarioResponse(
        id=usuario.id,
        username=usuario.username,
        email=usuario.email,
        activo=usuario.activo,
    )
