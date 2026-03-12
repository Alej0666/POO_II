"""Enumeraciones del dominio del sistema TaskFlow."""

from enum import Enum


class PrioridadTarea(Enum):
    """Niveles de prioridad para las tareas.

    Attributes:
        ALTA: Prioridad alta, valor 1.
        MEDIA: Prioridad media, valor 2.
        BAJA: Prioridad baja, valor 3.
    """

    ALTA = 1
    MEDIA = 2
    BAJA = 3


class EstadoTarea(Enum):
    """Estados posibles de una tarea.

    Attributes:
        PENDIENTE: La tarea aún no ha sido iniciada.
        EN_PROGRESO: La tarea está siendo trabajada.
        COMPLETADA: La tarea ha sido finalizada.
    """

    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
