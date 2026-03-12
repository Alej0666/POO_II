"""Fixtures compartidas para los tests de TaskFlow."""

import pytest

from src.domain.enums import EstadoTarea, PrioridadTarea
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.usuario import Usuario


@pytest.fixture
def usuario_ejemplo() -> Usuario:
    """Usuario válido para pruebas."""
    return Usuario(
        username="testuser",
        email="test@example.com",
        nombre_completo="Usuario de Prueba",
    )


@pytest.fixture
def proyecto_ejemplo(usuario_ejemplo: Usuario) -> Proyecto:
    """Proyecto con líder para pruebas."""
    return Proyecto(
        nombre="Proyecto Test",
        lider=usuario_ejemplo,
        descripcion="Descripción de prueba",
    )


@pytest.fixture
def tarea_ejemplo() -> Tarea:
    """Tarea pendiente por defecto para pruebas."""
    return Tarea(
        titulo="Tarea de prueba",
        prioridad=PrioridadTarea.MEDIA,
        descripcion="Descripción de prueba",
    )


@pytest.fixture
def proyecto_con_tareas(proyecto_ejemplo: Proyecto, tarea_ejemplo: Tarea) -> Proyecto:
    """Proyecto con una tarea ya agregada."""
    proyecto_ejemplo.agregar_tarea(tarea_ejemplo)
    return proyecto_ejemplo
