"""Tests unitarios para los enums PrioridadTarea y EstadoTarea."""

import pytest
from enum import Enum

from src.domain.enums import EstadoTarea, PrioridadTarea


class TestPrioridadTarea:
    """Tests para el enum PrioridadTarea."""

    def test_es_enum(self) -> None:
        """PrioridadTarea debe ser subclase de Enum."""
        assert issubclass(PrioridadTarea, Enum)

    @pytest.mark.parametrize(
        "miembro, valor_esperado",
        [
            (PrioridadTarea.ALTA, 1),
            (PrioridadTarea.MEDIA, 2),
            (PrioridadTarea.BAJA, 3),
        ],
    )
    def test_valores_correctos(
        self, miembro: PrioridadTarea, valor_esperado: int
    ) -> None:
        """Cada miembro de PrioridadTarea tiene el valor entero correcto."""
        assert miembro.value == valor_esperado

    def test_tiene_tres_miembros(self) -> None:
        """PrioridadTarea tiene exactamente 3 miembros."""
        assert len(PrioridadTarea) == 3

    @pytest.mark.parametrize(
        "nombre",
        ["ALTA", "MEDIA", "BAJA"],
    )
    def test_acceso_por_nombre(self, nombre: str) -> None:
        """Los miembros son accesibles por nombre."""
        assert PrioridadTarea[nombre] is not None

    def test_ordenamiento_por_valor(self) -> None:
        """ALTA < MEDIA < BAJA según los valores enteros."""
        assert PrioridadTarea.ALTA.value < PrioridadTarea.MEDIA.value
        assert PrioridadTarea.MEDIA.value < PrioridadTarea.BAJA.value


class TestEstadoTarea:
    """Tests para el enum EstadoTarea."""

    def test_es_enum(self) -> None:
        """EstadoTarea debe ser subclase de Enum."""
        assert issubclass(EstadoTarea, Enum)

    @pytest.mark.parametrize(
        "miembro, valor_esperado",
        [
            (EstadoTarea.PENDIENTE, "pendiente"),
            (EstadoTarea.EN_PROGRESO, "en_progreso"),
            (EstadoTarea.COMPLETADA, "completada"),
        ],
    )
    def test_valores_son_strings(
        self, miembro: EstadoTarea, valor_esperado: str
    ) -> None:
        """Cada miembro de EstadoTarea tiene el valor de cadena correcto."""
        assert miembro.value == valor_esperado

    def test_tiene_tres_miembros(self) -> None:
        """EstadoTarea tiene exactamente 3 miembros."""
        assert len(EstadoTarea) == 3

    @pytest.mark.parametrize(
        "nombre",
        ["PENDIENTE", "EN_PROGRESO", "COMPLETADA"],
    )
    def test_acceso_por_nombre(self, nombre: str) -> None:
        """Los miembros son accesibles por nombre."""
        assert EstadoTarea[nombre] is not None

    def test_miembros_son_distintos(self) -> None:
        """Los tres estados son objetos distintos (no iguales entre sí)."""
        assert EstadoTarea.PENDIENTE != EstadoTarea.EN_PROGRESO
        assert EstadoTarea.EN_PROGRESO != EstadoTarea.COMPLETADA
        assert EstadoTarea.PENDIENTE != EstadoTarea.COMPLETADA
