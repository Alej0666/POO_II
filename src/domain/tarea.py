"""Módulo que define la clase Tarea del sistema TaskFlow."""

from datetime import datetime
from typing import Optional

from src.domain.enums import EstadoTarea, PrioridadTarea


class Tarea:
    """Representa una tarea individual dentro de un proyecto TaskFlow.

    Una tarea tiene un estado (PENDIENTE, EN_PROGRESO, COMPLETADA) y una
    prioridad (ALTA, MEDIA, BAJA) que pueden cambiar a lo largo de su
    ciclo de vida.

    Attributes:
        titulo: Título descriptivo de la tarea.
        descripcion: Detalles adicionales de la tarea (opcional).
        prioridad: Nivel de prioridad de la tarea.
        estado: Estado actual de la tarea.
        fecha_creacion: Fecha y hora en que se creó la tarea.
        fecha_completado: Fecha y hora en que se completó (opcional).
    """

    def __init__(
        self,
        titulo: str,
        prioridad: PrioridadTarea,
        descripcion: Optional[str] = None,
    ) -> None:
        """Inicializa una nueva tarea.

        Args:
            titulo: Título de la tarea, mínimo 3 caracteres.
            prioridad: Nivel de prioridad inicial de la tarea.
            descripcion: Descripción detallada opcional.

        Raises:
            ValueError: Si el título tiene menos de 3 caracteres.
            ValueError: Si la prioridad no es una instancia de PrioridadTarea.
        """
        if len(titulo) < 3:
            raise ValueError(
                f"El título '{titulo}' debe tener al menos 3 caracteres."
            )
        if not isinstance(prioridad, PrioridadTarea):
            raise ValueError(
                f"La prioridad debe ser una instancia de PrioridadTarea, "
                f"no '{type(prioridad).__name__}'."
            )

        self._titulo: str = titulo
        self._prioridad: PrioridadTarea = prioridad
        self.descripcion: Optional[str] = descripcion
        self._estado: EstadoTarea = EstadoTarea.PENDIENTE
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_completado: Optional[datetime] = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def titulo(self) -> str:
        """Título de la tarea."""
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        """Valida y asigna el título.

        Args:
            valor: Nuevo título de la tarea.

        Raises:
            ValueError: Si el título tiene menos de 3 caracteres.
        """
        if len(valor) < 3:
            raise ValueError(
                f"El título '{valor}' debe tener al menos 3 caracteres."
            )
        self._titulo = valor

    @property
    def prioridad(self) -> PrioridadTarea:
        """Prioridad actual de la tarea."""
        return self._prioridad

    @property
    def estado(self) -> EstadoTarea:
        """Estado actual de la tarea."""
        return self._estado

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def iniciar(self) -> None:
        """Cambia el estado de la tarea a EN_PROGRESO.

        Raises:
            ValueError: Si la tarea ya está completada.
        """
        if self._estado == EstadoTarea.COMPLETADA:
            raise ValueError(
                "No se puede iniciar una tarea que ya está completada."
            )
        self._estado = EstadoTarea.EN_PROGRESO

    def completar(self) -> None:
        """Marca la tarea como completada y registra la fecha.

        Raises:
            ValueError: Si la tarea ya estaba completada previamente.
        """
        if self._estado == EstadoTarea.COMPLETADA:
            raise ValueError("La tarea ya está completada.")
        self._estado = EstadoTarea.COMPLETADA
        self.fecha_completado = datetime.now()

    def cambiar_prioridad(self, nueva_prioridad: PrioridadTarea) -> None:
        """Cambia la prioridad de la tarea.

        Args:
            nueva_prioridad: Nueva prioridad a asignar.

        Raises:
            ValueError: Si nueva_prioridad no es una instancia de PrioridadTarea.
        """
        if not isinstance(nueva_prioridad, PrioridadTarea):
            raise ValueError(
                f"La prioridad debe ser una instancia de PrioridadTarea, "
                f"no '{type(nueva_prioridad).__name__}'."
            )
        self._prioridad = nueva_prioridad

    # ------------------------------------------------------------------
    # Métodos especiales
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Retorna la representación informal de la tarea.

        Returns:
            String con el formato '[PRIORIDAD] titulo (estado)'.
        """
        return (
            f"[{self._prioridad.name}] {self._titulo} ({self._estado.value})"
        )

    def __repr__(self) -> str:
        """Retorna la representación oficial de la tarea.

        Returns:
            String con el formato "Tarea('titulo', prioridad, estado)".
        """
        return (
            f"Tarea('{self._titulo}', {self._prioridad!r}, {self._estado!r})"
        )
