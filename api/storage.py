# -*- coding: utf-8 -*-
"""Almacenamiento en memoria para la API de TaskFlow.

Los datos se pierden al reiniciar (se reemplazará con persistencia en E4).
"""

from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.usuario import Usuario

# Dicts principales: id (int) -> objeto de dominio
usuarios_db: dict[int, Usuario] = {}
proyectos_db: dict[int, Proyecto] = {}
tareas_db: dict[int, Tarea] = {}

# Contadores de IDs autoincrement
_usuario_counter: int = 0
_proyecto_counter: int = 0
_tarea_counter: int = 0


def next_usuario_id() -> int:
    global _usuario_counter
    _usuario_counter += 1
    return _usuario_counter


def next_proyecto_id() -> int:
    global _proyecto_counter
    _proyecto_counter += 1
    return _proyecto_counter


def next_tarea_id() -> int:
    global _tarea_counter
    _tarea_counter += 1
    return _tarea_counter
