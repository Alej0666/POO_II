"""Tests unitarios para la clase Proyecto del sistema TaskFlow."""

import pytest
from datetime import datetime

from src.domain.enums import EstadoTarea, PrioridadTarea
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.usuario import Usuario


class TestProyectoCreacion:
    """Tests para la creación de proyectos."""

    def test_crear_proyecto_valido(
        self, proyecto_ejemplo: Proyecto, usuario_ejemplo: Usuario
    ) -> None:
        """Un proyecto válido se crea con atributos correctos y sin tareas."""
        assert proyecto_ejemplo.nombre == "Proyecto Test"
        assert proyecto_ejemplo.lider == usuario_ejemplo
        assert proyecto_ejemplo.descripcion == "Descripción de prueba"
        assert proyecto_ejemplo.tareas == []
        assert isinstance(proyecto_ejemplo.fecha_creacion, datetime)

    def test_crear_proyecto_sin_descripcion(
        self, usuario_ejemplo: Usuario
    ) -> None:
        """Crear proyecto sin descripción es válido (campo opcional)."""
        p = Proyecto(nombre="Sin desc", lider=usuario_ejemplo)
        assert p.descripcion is None

    def test_nombre_muy_corto_lanza_error(
        self, usuario_ejemplo: Usuario
    ) -> None:
        """Nombres con menos de 3 caracteres lanzan ValueError."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Proyecto(nombre="AB", lider=usuario_ejemplo)

    @pytest.mark.parametrize(
        "lider_invalido",
        ["no_es_usuario", 123, None, []],
    )
    def test_lider_tipo_invalido_lanza_error(
        self, lider_invalido: object
    ) -> None:
        """Un líder que no es instancia de Usuario lanza ValueError."""
        with pytest.raises(ValueError, match="instancia de Usuario"):
            Proyecto(nombre="Nombre valido", lider=lider_invalido)  # type: ignore[arg-type]


class TestProyectoTareas:
    """Tests para agregar y gestionar tareas en un proyecto."""

    def test_agregar_tarea(
        self, proyecto_ejemplo: Proyecto, tarea_ejemplo: Tarea
    ) -> None:
        """agregar_tarea() incorpora la tarea a la lista del proyecto."""
        proyecto_ejemplo.agregar_tarea(tarea_ejemplo)
        assert tarea_ejemplo in proyecto_ejemplo.tareas

    def test_agregar_multiple_tareas(self, proyecto_ejemplo: Proyecto) -> None:
        """Se pueden agregar varias tareas distintas al mismo proyecto."""
        t1 = Tarea("Primera tarea", PrioridadTarea.ALTA)
        t2 = Tarea("Segunda tarea", PrioridadTarea.BAJA)
        proyecto_ejemplo.agregar_tarea(t1)
        proyecto_ejemplo.agregar_tarea(t2)
        assert len(proyecto_ejemplo.tareas) == 2

    def test_agregar_tarea_duplicada_lanza_error(
        self, proyecto_con_tareas: Proyecto, tarea_ejemplo: Tarea
    ) -> None:
        """Agregar la misma tarea dos veces lanza ValueError."""
        with pytest.raises(ValueError, match="ya existe en el proyecto"):
            proyecto_con_tareas.agregar_tarea(tarea_ejemplo)

    def test_agregar_tarea_none_lanza_error(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """Pasar None como tarea lanza ValueError."""
        with pytest.raises(ValueError, match="no puede ser None"):
            proyecto_ejemplo.agregar_tarea(None)  # type: ignore[arg-type]

    def test_agregar_tipo_incorrecto_lanza_error(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """Pasar un objeto que no es Tarea lanza ValueError."""
        with pytest.raises(ValueError, match="instancia de Tarea"):
            proyecto_ejemplo.agregar_tarea("no_es_tarea")  # type: ignore[arg-type]

    def test_tareas_retorna_copia_defensiva(
        self, proyecto_con_tareas: Proyecto
    ) -> None:
        """Modificar la lista retornada por tareas no altera el proyecto."""
        copia = proyecto_con_tareas.tareas
        copia.clear()
        assert len(proyecto_con_tareas.tareas) == 1


class TestProyectoFiltros:
    """Tests para los métodos de filtrado de tareas."""

    def test_obtener_tareas_pendientes_excluye_completadas(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """obtener_tareas_pendientes() excluye tareas con estado COMPLETADA."""
        t_pendiente = Tarea("Tarea pendiente", PrioridadTarea.MEDIA)
        t_completada = Tarea("Tarea completada", PrioridadTarea.BAJA)
        t_completada.completar()
        proyecto_ejemplo.agregar_tarea(t_pendiente)
        proyecto_ejemplo.agregar_tarea(t_completada)

        pendientes = proyecto_ejemplo.obtener_tareas_pendientes()
        assert t_pendiente in pendientes
        assert t_completada not in pendientes

    def test_obtener_tareas_pendientes_incluye_en_progreso(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """obtener_tareas_pendientes() incluye tareas EN_PROGRESO."""
        t = Tarea("En progreso", PrioridadTarea.ALTA)
        t.iniciar()
        proyecto_ejemplo.agregar_tarea(t)

        assert t in proyecto_ejemplo.obtener_tareas_pendientes()

    def test_obtener_tareas_pendientes_proyecto_vacio(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """obtener_tareas_pendientes() retorna lista vacía si no hay tareas."""
        assert proyecto_ejemplo.obtener_tareas_pendientes() == []

    def test_obtener_tareas_por_prioridad(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """obtener_tareas_por_prioridad() filtra correctamente por prioridad."""
        t_alta = Tarea("Tarea alta", PrioridadTarea.ALTA)
        t_baja = Tarea("Tarea baja", PrioridadTarea.BAJA)
        proyecto_ejemplo.agregar_tarea(t_alta)
        proyecto_ejemplo.agregar_tarea(t_baja)

        altas = proyecto_ejemplo.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
        assert t_alta in altas
        assert t_baja not in altas

    def test_obtener_tareas_por_prioridad_sin_coincidencias(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """obtener_tareas_por_prioridad() retorna lista vacía si no hay coincidencias."""
        t = Tarea("Tarea baja", PrioridadTarea.BAJA)
        proyecto_ejemplo.agregar_tarea(t)

        assert proyecto_ejemplo.obtener_tareas_por_prioridad(PrioridadTarea.ALTA) == []

    def test_obtener_tareas_por_prioridad_invalida_lanza_error(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """obtener_tareas_por_prioridad() con tipo incorrecto lanza ValueError."""
        with pytest.raises(ValueError, match="instancia de PrioridadTarea"):
            proyecto_ejemplo.obtener_tareas_por_prioridad("ALTA")  # type: ignore[arg-type]


class TestProyectoRepresentacion:
    """Tests para __str__, __repr__ y el setter de nombre."""

    def test_str_retorna_nombre(self, proyecto_ejemplo: Proyecto) -> None:
        """__str__ retorna el nombre del proyecto."""
        assert str(proyecto_ejemplo) == "Proyecto Test"

    def test_repr_formato_correcto(self, proyecto_ejemplo: Proyecto) -> None:
        """__repr__ incluye el nombre del proyecto."""
        assert "Proyecto Test" in repr(proyecto_ejemplo)

    def test_nombre_setter_valido(self, proyecto_ejemplo: Proyecto) -> None:
        """El nombre puede cambiarse a uno válido."""
        proyecto_ejemplo.nombre = "Nombre Nuevo"
        assert proyecto_ejemplo.nombre == "Nombre Nuevo"

    def test_nombre_setter_corto_lanza_error(
        self, proyecto_ejemplo: Proyecto
    ) -> None:
        """El setter de nombre rechaza valores con menos de 3 caracteres."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            proyecto_ejemplo.nombre = "AB"
