"""Tests unitarios para la clase Tarea del sistema TaskFlow."""

import pytest
from datetime import datetime

from src.domain.enums import EstadoTarea, PrioridadTarea
from src.domain.tarea import Tarea


class TestTareaCreacion:
    """Tests para la creación de tareas."""

    def test_crear_tarea_valida(self, tarea_ejemplo: Tarea) -> None:
        """Una tarea válida inicia en estado PENDIENTE sin fecha de completado."""
        assert tarea_ejemplo.titulo == "Tarea de prueba"
        assert tarea_ejemplo.prioridad == PrioridadTarea.MEDIA
        assert tarea_ejemplo.estado == EstadoTarea.PENDIENTE
        assert tarea_ejemplo.fecha_completado is None
        assert isinstance(tarea_ejemplo.fecha_creacion, datetime)

    def test_crear_tarea_sin_descripcion(self) -> None:
        """Crear tarea sin descripción es válido (campo opcional)."""
        t = Tarea(titulo="Sin descripcion", prioridad=PrioridadTarea.BAJA)
        assert t.descripcion is None

    @pytest.mark.parametrize(
        "titulo_invalido",
        ["", "AB", "  "],
    )
    def test_titulo_muy_corto_lanza_error(self, titulo_invalido: str) -> None:
        """Títulos con menos de 3 caracteres lanzan ValueError."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Tarea(titulo=titulo_invalido, prioridad=PrioridadTarea.ALTA)

    def test_prioridad_tipo_invalido_lanza_error(self) -> None:
        """Pasar un tipo incorrecto como prioridad lanza ValueError."""
        with pytest.raises(ValueError, match="instancia de PrioridadTarea"):
            Tarea(titulo="Titulo valido", prioridad="ALTA")  # type: ignore[arg-type]


class TestTareaEstados:
    """Tests para los cambios de estado de una tarea."""

    def test_iniciar_tarea_pendiente(self, tarea_ejemplo: Tarea) -> None:
        """iniciar() cambia el estado a EN_PROGRESO desde PENDIENTE."""
        tarea_ejemplo.iniciar()
        assert tarea_ejemplo.estado == EstadoTarea.EN_PROGRESO

    def test_completar_tarea_pendiente(self, tarea_ejemplo: Tarea) -> None:
        """completar() cambia el estado a COMPLETADA y registra fecha."""
        tarea_ejemplo.completar()
        assert tarea_ejemplo.estado == EstadoTarea.COMPLETADA
        assert isinstance(tarea_ejemplo.fecha_completado, datetime)

    def test_completar_tarea_en_progreso(self, tarea_ejemplo: Tarea) -> None:
        """completar() desde EN_PROGRESO también funciona correctamente."""
        tarea_ejemplo.iniciar()
        tarea_ejemplo.completar()
        assert tarea_ejemplo.estado == EstadoTarea.COMPLETADA

    def test_completar_tarea_ya_completada_lanza_error(
        self, tarea_ejemplo: Tarea
    ) -> None:
        """completar() sobre una tarea ya completada lanza ValueError."""
        tarea_ejemplo.completar()
        with pytest.raises(ValueError, match="ya está completada"):
            tarea_ejemplo.completar()

    def test_iniciar_tarea_completada_lanza_error(
        self, tarea_ejemplo: Tarea
    ) -> None:
        """iniciar() sobre una tarea completada lanza ValueError."""
        tarea_ejemplo.completar()
        with pytest.raises(ValueError, match="ya está completada"):
            tarea_ejemplo.iniciar()

    def test_fecha_completado_none_mientras_pendiente(
        self, tarea_ejemplo: Tarea
    ) -> None:
        """fecha_completado permanece None hasta que la tarea se complete."""
        tarea_ejemplo.iniciar()
        assert tarea_ejemplo.fecha_completado is None


class TestTareaPrioridad:
    """Tests para cambiar la prioridad de una tarea."""

    @pytest.mark.parametrize(
        "nueva_prioridad",
        [PrioridadTarea.ALTA, PrioridadTarea.MEDIA, PrioridadTarea.BAJA],
    )
    def test_cambiar_prioridad_valida(
        self, tarea_ejemplo: Tarea, nueva_prioridad: PrioridadTarea
    ) -> None:
        """cambiar_prioridad() acepta cualquier valor de PrioridadTarea."""
        tarea_ejemplo.cambiar_prioridad(nueva_prioridad)
        assert tarea_ejemplo.prioridad == nueva_prioridad

    def test_cambiar_prioridad_tipo_invalido_lanza_error(
        self, tarea_ejemplo: Tarea
    ) -> None:
        """cambiar_prioridad() con tipo incorrecto lanza ValueError."""
        with pytest.raises(ValueError, match="instancia de PrioridadTarea"):
            tarea_ejemplo.cambiar_prioridad("BAJA")  # type: ignore[arg-type]

    def test_cambiar_prioridad_a_none_lanza_error(
        self, tarea_ejemplo: Tarea
    ) -> None:
        """cambiar_prioridad() con None lanza ValueError."""
        with pytest.raises(ValueError):
            tarea_ejemplo.cambiar_prioridad(None)  # type: ignore[arg-type]


class TestTareaRepresentacion:
    """Tests para __str__, __repr__ y el setter de título."""

    def test_str_formato_correcto(self, tarea_ejemplo: Tarea) -> None:
        """__str__ retorna '[PRIORIDAD] titulo (estado)'."""
        assert str(tarea_ejemplo) == "[MEDIA] Tarea de prueba (pendiente)"

    def test_repr_formato_correcto(self, tarea_ejemplo: Tarea) -> None:
        """__repr__ incluye título, prioridad y estado."""
        resultado = repr(tarea_ejemplo)
        assert "Tarea de prueba" in resultado
        assert "MEDIA" in resultado
        assert "PENDIENTE" in resultado

    def test_titulo_setter_valido(self, tarea_ejemplo: Tarea) -> None:
        """El título puede cambiarse a uno válido."""
        tarea_ejemplo.titulo = "Nuevo titulo"
        assert tarea_ejemplo.titulo == "Nuevo titulo"

    def test_titulo_setter_corto_lanza_error(self, tarea_ejemplo: Tarea) -> None:
        """El setter de título rechaza valores con menos de 3 caracteres."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            tarea_ejemplo.titulo = "AB"
