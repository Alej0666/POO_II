# -*- coding: utf-8 -*-
"""Rutas de la API para Usuarios — Con AsyncSession + JWT (E5)."""

from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Usuario
from api.schemas.usuario import UsuarioOut, UsuarioUpdate
from api.services.usuario_service import UsuarioService
from api.auth import get_current_user

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


@router.get("", response_model=list[UsuarioOut], summary="Listar usuarios")
async def listar_usuarios(session: AsyncSession = Depends(get_db)):
    """Retorna lista de usuarios desde BD."""
    stmt = select(Usuario).order_by(Usuario.id)
    result = await session.execute(stmt)
    usuarios = result.scalars().all()
    return usuarios


@router.get("/opciones", response_class=HTMLResponse, include_in_schema=False)
async def opciones_usuarios(session: AsyncSession = Depends(get_db)):
    """Opciones <option> para select de líder (HTMX)."""
    return HTMLResponse(await _get_opciones_usuarios(session))


@router.get("/{usuario_id}", response_model=UsuarioOut, summary="Obtener usuario por ID")
async def obtener_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Obtiene un usuario por ID."""
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioOut, summary="Actualizar usuario")
async def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualiza datos de un usuario (solo el propietario)."""
    # Validar propiedad
    if current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este usuario",
        )
    
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    # Actualizar campos proporcionados
    if data.email is not None:
        usuario.email = data.email
    if data.nombre_completo is not None:
        usuario.nombre_completo = data.nombre_completo
    if data.activo is not None:
        usuario.activo = data.activo
    
    await session.commit()
    await session.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario")
async def eliminar_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Elimina un usuario (solo el propietario)."""
    # Validar propiedad
    if current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este usuario",
        )
    
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    await session.delete(usuario)
    await session.commit()

