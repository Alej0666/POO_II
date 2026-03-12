"""Tests básicos para el dominio del sistema TaskFlow."""

import pytest
from datetime import datetime

from src.domain.enums import EstadoTarea, PrioridadTarea
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto


# ======================================================================
# Fixtures
# ======================================================================


@pytest.fixture
def usuario_valido() -> Usuario:
    """Retorna un usuario válido para reutilizar en tests."""
    return Usuario("juandev", "juan@example.com", "Juan Pérez")


@pytest.fixture
def tarea_valida() -> Tarea:
    """Retorna una tarea válida para reutilizar en tests."""
    return Tarea("Implementar login", PrioridadTarea.ALTA)


@pytest.fixture
def proyecto_valido(usuario_valido: Usuario) -> Proyecto:
    """Retorna un proyecto válido para reutilizar en tests."""
    return Proyecto("TaskFlow", usuario_valido, "Sistema de gestión de tareas")


# ======================================================================
# Tests: Usuario
# ======================================================================


class TestUsuario:
    """Pruebas para la clase Usuario."""

    def test_crear_usuario_valido(self) -> None:
        """Debe crear un usuario con datos válidos."""
        u = Usuario("ana123", "ana@test.com")
        assert u.username == "ana123"
        assert u.email == "ana@test.com"
        assert u.activo is True
        assert isinstance(u.fecha_registro, datetime)

    def test_str_retorna_arroba_username(self, usuario_valido: Usuario) -> None:
        """__str__ debe retornar '@username'."""
        assert str(usuario_valido) == "@juandev"

    def test_repr_formato_correcto(self, usuario_valido: Usuario) -> None:
        """__repr__ debe retornar "Usuario('username', 'email')"."""
        assert repr(usuario_valido) == "Usuario('juandev', 'juan@example.com')"

    def test_username_inmutable(self, usuario_valido: Usuario) -> None:
        """El username no debe poder modificarse."""
        with pytest.raises(AttributeError):
            usuario_valido.username = "otro"  # type: ignore[misc]

    def test_activar_desactivar(self, usuario_valido: Usuario) -> None:
        """Activar y desactivar deben cambiar el estado correctamente."""
        usuario_valido.desactivar()
        assert usuario_valido.activo is False
        usuario_valido.activar()
        assert usuario_valido.activo is True

    def test_username_demasiado_corto(self) -> None:
        """Debe lanzar ValueError si username tiene menos de 3 caracteres."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Usuario("ab", "ab@test.com")

    def test_username_con_caracteres_especiales(self) -> None:
        """Debe lanzar ValueError si username contiene caracteres no alfanuméricos."""
        with pytest.raises(ValueError, match="solo puede contener"):
            Usuario("us@r", "user@test.com")

    def test_email_sin_arroba(self) -> None:
        """Debe lanzar ValueError si el email no contiene '@'."""
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario("usuario", "emailsinaarroba.com")

    def test_email_sin_punto(self) -> None:
        """Debe lanzar ValueError si el email no contiene '.'."""
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario("usuario", "email@sinpunto")

    def test_cambiar_email_valido(self, usuario_valido: Usuario) -> None:
        """Debe permitir cambiar el email a uno válido."""
        usuario_valido.email = "nuevo@correo.org"
        assert usuario_valido.email == "nuevo@correo.org"


# ======================================================================
# Tests: Tarea
# ======================================================================


class TestTarea:
    """Pruebas para la clase Tarea."""

    def test_crear_tarea_valida(self) -> None:
        """Debe crear una tarea con estado inicial PENDIENTE."""
        t = Tarea("Diseñar base de datos", PrioridadTarea.MEDIA)
        assert t.titulo == "Diseñar base de datos"
        assert t.prioridad == PrioridadTarea.MEDIA
        assert t.estado == EstadoTarea.PENDIENTE
        assert t.fecha_completado is None

    def test_str_formato_correcto(self, tarea_valida: Tarea) -> None:
        """__str__ debe retornar '[PRIORIDAD] titulo (estado)'."""
        assert str(tarea_valida) == "[ALTA] Implementar login (pendiente)"

    def test_iniciar_tarea(self, tarea_valida: Tarea) -> None:
        """iniciar() debe cambiar el estado a EN_PROGRESO."""
        tarea_valida.iniciar()
        assert tarea_valida.estado == EstadoTarea.EN_PROGRESO

    def test_completar_tarea(self, tarea_valida: Tarea) -> None:
        """completar() debe cambiar el estado a COMPLETADA y registrar fecha."""
        tarea_valida.completar()
        assert tarea_valida.estado == EstadoTarea.COMPLETADA
        assert isinstance(tarea_valida.fecha_completado, datetime)

    def test_completar_tarea_ya_completada(self, tarea_valida: Tarea) -> None:
        """completar() debe lanzar ValueError si la tarea ya está completada."""
        tarea_valida.completar()
        with pytest.raises(ValueError, match="ya está completada"):
            tarea_valida.completar()

    def test_iniciar_tarea_completada(self, tarea_valida: Tarea) -> None:
        """iniciar() debe lanzar ValueError si la tarea ya está completada."""
        tarea_valida.completar()
        with pytest.raises(ValueError, match="ya está completada"):
            tarea_valida.iniciar()

    def test_cambiar_prioridad(self, tarea_valida: Tarea) -> None:
        """cambiar_prioridad() debe actualizar la prioridad correctamente."""
        tarea_valida.cambiar_prioridad(PrioridadTarea.BAJA)
        assert tarea_valida.prioridad == PrioridadTarea.BAJA

    def test_cambiar_prioridad_valor_invalido(self, tarea_valida: Tarea) -> None:
        """cambiar_prioridad() debe lanzar ValueError si el valor no es válido."""
        with pytest.raises(ValueError):
            tarea_valida.cambiar_prioridad("ALTA")  # type: ignore[arg-type]

    def test_titulo_demasiado_corto(self) -> None:
        """Debe lanzar ValueError si el título tiene menos de 3 caracteres."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Tarea("AB", PrioridadTarea.BAJA)


# ======================================================================
# Tests: Proyecto
# ======================================================================


class TestProyecto:
    """Pruebas para la clase Proyecto."""

    def test_crear_proyecto_valido(
        self, proyecto_valido: Proyecto, usuario_valido: Usuario
    ) -> None:
        """Debe crear un proyecto con datos válidos y lista de tareas vacía."""
        assert proyecto_valido.nombre == "TaskFlow"
        assert proyecto_valido.lider == usuario_valido
        assert proyecto_valido.tareas == []
        assert isinstance(proyecto_valido.fecha_creacion, datetime)

    def test_str_retorna_nombre(self, proyecto_valido: Proyecto) -> None:
        """__str__ debe retornar el nombre del proyecto."""
        assert str(proyecto_valido) == "TaskFlow"

    def test_agregar_tarea(
        self, proyecto_valido: Proyecto, tarea_valida: Tarea
    ) -> None:
        """agregar_tarea() debe agregar la tarea a la lista."""
        proyecto_valido.agregar_tarea(tarea_valida)
        assert tarea_valida in proyecto_valido.tareas

    def test_agregar_tarea_duplicada(
        self, proyecto_valido: Proyecto, tarea_valida: Tarea
    ) -> None:
        """agregar_tarea() debe lanzar ValueError si la tarea ya existe."""
        proyecto_valido.agregar_tarea(tarea_valida)
        with pytest.raises(ValueError, match="ya existe en el proyecto"):
            proyecto_valido.agregar_tarea(tarea_valida)

    def test_agregar_tarea_none(self, proyecto_valido: Proyecto) -> None:
        """agregar_tarea() debe lanzar ValueError si se pasa None."""
        with pytest.raises(ValueError, match="no puede ser None"):
            proyecto_valido.agregar_tarea(None)  # type: ignore[arg-type]

    def test_obtener_tareas_pendientes(self, proyecto_valido: Proyecto) -> None:
        """obtener_tareas_pendientes() debe excluir las tareas completadas."""
        t1 = Tarea("Tarea uno", PrioridadTarea.ALTA)
        t2 = Tarea("Tarea dos", PrioridadTarea.BAJA)
        t2.completar()
        proyecto_valido.agregar_tarea(t1)
        proyecto_valido.agregar_tarea(t2)

        pendientes = proyecto_valido.obtener_tareas_pendientes()
        assert t1 in pendientes
        assert t2 not in pendientes

    def test_obtener_tareas_por_prioridad(
        self, proyecto_valido: Proyecto
    ) -> None:
        """obtener_tareas_por_prioridad() debe filtrar correctamente."""
        t_alta = Tarea("Tarea alta", PrioridadTarea.ALTA)
        t_baja = Tarea("Tarea baja", PrioridadTarea.BAJA)
        proyecto_valido.agregar_tarea(t_alta)
        proyecto_valido.agregar_tarea(t_baja)

        altas = proyecto_valido.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
        assert t_alta in altas
        assert t_baja not in altas

    def test_nombre_demasiado_corto(self, usuario_valido: Usuario) -> None:
        """Debe lanzar ValueError si el nombre tiene menos de 3 caracteres."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Proyecto("AB", usuario_valido)

    def test_lider_invalido(self) -> None:
        """Debe lanzar ValueError si el líder no es una instancia de Usuario."""
        with pytest.raises(ValueError, match="instancia de Usuario"):
            Proyecto("Proyecto X", "no_es_usuario")  # type: ignore[arg-type]
