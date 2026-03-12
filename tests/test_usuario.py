"""Tests unitarios para la clase Usuario del sistema TaskFlow."""

import pytest
from datetime import datetime

from src.domain.usuario import Usuario


class TestUsuarioCreacion:
    """Tests para la creación de usuarios."""

    def test_crear_usuario_valido(self, usuario_ejemplo: Usuario) -> None:
        """Un usuario válido se crea con los atributos correctos."""
        assert usuario_ejemplo.username == "testuser"
        assert usuario_ejemplo.email == "test@example.com"
        assert usuario_ejemplo.nombre_completo == "Usuario de Prueba"
        assert usuario_ejemplo.activo is True
        assert isinstance(usuario_ejemplo.fecha_registro, datetime)

    def test_crear_usuario_sin_nombre_completo(self) -> None:
        """Crear usuario sin nombre_completo es válido (campo opcional)."""
        u = Usuario(username="noname", email="noname@test.com")
        assert u.nombre_completo is None

    @pytest.mark.parametrize(
        "username_invalido, fragmento_error",
        [
            ("ab", "al menos 3 caracteres"),
            ("", "al menos 3 caracteres"),
            ("user@name", "solo puede contener"),
            ("user.name", "solo puede contener"),
            ("user name", "solo puede contener"),
        ],
    )
    def test_username_invalido_lanza_error(
        self, username_invalido: str, fragmento_error: str
    ) -> None:
        """Usernames inválidos lanzan ValueError con mensaje apropiado."""
        with pytest.raises(ValueError, match=fragmento_error):
            Usuario(username=username_invalido, email="test@test.com")

    @pytest.mark.parametrize(
        "email_invalido",
        [
            "emailsinpunto",
            "emailsinarroba.com",
            "sinambos",
            "@sindominio",
        ],
    )
    def test_email_invalido_lanza_error(self, email_invalido: str) -> None:
        """Emails inválidos lanzan ValueError con 'Email inválido'."""
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(username="valido", email=email_invalido)


class TestUsuarioEstado:
    """Tests para activar y desactivar un usuario."""

    def test_usuario_activo_al_crearse(self, usuario_ejemplo: Usuario) -> None:
        """Un usuario recién creado debe estar activo."""
        assert usuario_ejemplo.activo is True

    def test_desactivar_usuario(self, usuario_ejemplo: Usuario) -> None:
        """desactivar() pone activo en False."""
        usuario_ejemplo.desactivar()
        assert usuario_ejemplo.activo is False

    def test_activar_usuario_desactivado(self, usuario_ejemplo: Usuario) -> None:
        """activar() pone activo en True después de desactivar."""
        usuario_ejemplo.desactivar()
        usuario_ejemplo.activar()
        assert usuario_ejemplo.activo is True

    def test_activar_usuario_ya_activo(self, usuario_ejemplo: Usuario) -> None:
        """activar() sobre usuario ya activo no lanza error."""
        usuario_ejemplo.activar()
        assert usuario_ejemplo.activo is True


class TestUsuarioProperties:
    """Tests para las propiedades del usuario."""

    def test_username_es_inmutable(self, usuario_ejemplo: Usuario) -> None:
        """El username no puede modificarse tras la creación."""
        with pytest.raises(AttributeError):
            usuario_ejemplo.username = "otro"  # type: ignore[misc]

    def test_email_setter_valido(self, usuario_ejemplo: Usuario) -> None:
        """El email puede cambiarse a uno válido."""
        usuario_ejemplo.email = "nuevo@correo.org"
        assert usuario_ejemplo.email == "nuevo@correo.org"

    def test_email_setter_invalido_lanza_error(
        self, usuario_ejemplo: Usuario
    ) -> None:
        """Asignar un email inválido lanza ValueError."""
        with pytest.raises(ValueError, match="Email inválido"):
            usuario_ejemplo.email = "emailinvalido"


class TestUsuarioRepresentacion:
    """Tests para __str__ y __repr__."""

    def test_str_retorna_arroba_username(self, usuario_ejemplo: Usuario) -> None:
        """__str__ retorna '@username'."""
        assert str(usuario_ejemplo) == "@testuser"

    def test_repr_formato_correcto(self, usuario_ejemplo: Usuario) -> None:
        """__repr__ retorna "Usuario('username', 'email')"."""
        assert repr(usuario_ejemplo) == "Usuario('testuser', 'test@example.com')"
