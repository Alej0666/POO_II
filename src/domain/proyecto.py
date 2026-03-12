"""Módulo que define la clase Proyecto del sistema TaskFlow."""

from datetime import datetime
from typing import Optional

from src.domain.enums import EstadoTarea, PrioridadTarea
from src.domain.tarea import Tarea
from src.domain.usuario import Usuario


class Proyecto:
    """Agrupa múltiples tareas bajo un líder (Usuario).

    Relación de composición: el proyecto *posee* sus tareas. Si el
    proyecto se elimina, sus tareas deberían eliminarse también.

    Attributes:
        nombre: Nombre del proyecto.
        descripcion: Descripción opcional del proyecto.
        lider: Usuario responsable del proyecto.
        tareas: Lista de tareas asociadas al proyecto.
        fecha_creacion: Fecha y hora de creación del proyecto.
    """

    def __init__(
        self,
        nombre: str,
        lider: Usuario,
        descripcion: Optional[str] = None,
    ) -> None:
        """Inicializa un nuevo proyecto.

        Args:
            nombre: Nombre del proyecto, mínimo 3 caracteres.
            lider: Usuario que lidera el proyecto.
            descripcion: Descripción opcional del proyecto.

        Raises:
            ValueError: Si el nombre tiene menos de 3 caracteres.
            ValueError: Si el lider no es una instancia de Usuario.
        """
        if len(nombre) < 3:
            raise ValueError(
                f"El nombre '{nombre}' debe tener al menos 3 caracteres."
            )
        if not isinstance(lider, Usuario):
            raise ValueError(
                "El líder debe ser una instancia de Usuario, "
                f"no '{type(lider).__name__}'."
            )

        self._nombre: str = nombre
        self._lider: Usuario = lider
        self.descripcion: Optional[str] = descripcion
        self._tareas: list[Tarea] = []
        self.fecha_creacion: datetime = datetime.now()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def nombre(self) -> str:
        """Nombre del proyecto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del proyecto.

        Args:
            valor: Nuevo nombre del proyecto.

        Raises:
            ValueError: Si el nombre tiene menos de 3 caracteres.
        """
        if len(valor) < 3:
            raise ValueError(
                f"El nombre '{valor}' debe tener al menos 3 caracteres."
            )
        self._nombre = valor

    @property
    def lider(self) -> Usuario:
        """Usuario líder del proyecto."""
        return self._lider

    @property
    def tareas(self) -> list[Tarea]:
        """Lista de tareas del proyecto (copia defensiva)."""
        return list(self._tareas)

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def agregar_tarea(self, tarea: Tarea) -> None:
        """Agrega una tarea al proyecto.

        Args:
            tarea: La tarea a agregar. No puede ser None.

        Raises:
            ValueError: Si la tarea es None.
            ValueError: Si la tarea ya existe en el proyecto.
            ValueError: Si tarea no es una instancia de Tarea.
        """
        if tarea is None:
            raise ValueError("La tarea no puede ser None.")
        if not isinstance(tarea, Tarea):
            raise ValueError(
                "El argumento debe ser una instancia de Tarea, "
                f"no '{type(tarea).__name__}'."
            )
        if tarea in self._tareas:
            raise ValueError(
                f"La tarea '{tarea.titulo}' ya existe en el proyecto."
            )
        self._tareas.append(tarea)

    def obtener_tareas_pendientes(self) -> list[Tarea]:
        """Retorna todas las tareas que no han sido completadas.

        Returns:
            Lista de tareas cuyo estado es distinto de COMPLETADA.
        """
        return [
            t for t in self._tareas if t.estado != EstadoTarea.COMPLETADA
        ]

    def obtener_tareas_por_prioridad(
        self, prioridad: PrioridadTarea
    ) -> list[Tarea]:
        """Retorna las tareas que coinciden con la prioridad indicada.

        Args:
            prioridad: Nivel de prioridad por el que filtrar.

        Returns:
            Lista de tareas que tienen la prioridad especificada.

        Raises:
            ValueError: Si prioridad no es una instancia de PrioridadTarea.
        """
        if not isinstance(prioridad, PrioridadTarea):
            raise ValueError(
                "La prioridad debe ser una instancia de PrioridadTarea, "
                f"no '{type(prioridad).__name__}'."
            )
        return [t for t in self._tareas if t.prioridad == prioridad]

    # ------------------------------------------------------------------
    # Métodos especiales
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Retorna el nombre del proyecto.

        Returns:
            Nombre del proyecto como cadena de texto.
        """
        return self._nombre

    def __repr__(self) -> str:
        """Retorna la representación oficial del proyecto.

        Returns:
            String con el formato "Proyecto('nombre', lider)".
        """
        return f"Proyecto('{self._nombre}', {self._lider!r})"
