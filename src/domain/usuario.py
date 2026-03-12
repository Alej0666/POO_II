"""Módulo que define la clase Usuario del sistema TaskFlow."""

from datetime import datetime
from typing import Optional


class Usuario:
    """Representa un usuario en el sistema TaskFlow.

    Un usuario puede crear proyectos y tareas. Posee un identificador
    único (username) que es inmutable tras la creación.

    Attributes:
        username: Identificador único del usuario (inmutable).
        email: Correo electrónico validado.
        nombre_completo: Nombre completo del usuario (opcional).
        activo: Estado de la cuenta.
        fecha_registro: Fecha y hora de creación de la cuenta.
    """

    def __init__(
        self,
        username: str,
        email: str,
        nombre_completo: Optional[str] = None,
    ) -> None:
        """Inicializa un nuevo usuario.

        Args:
            username: Identificador único, mínimo 3 caracteres y
                solo caracteres alfanuméricos.
            email: Correo electrónico válido (debe contener '@' y '.').
            nombre_completo: Nombre real del usuario (opcional).

        Raises:
            ValueError: Si el username tiene menos de 3 caracteres.
            ValueError: Si el username contiene caracteres no alfanuméricos.
            ValueError: Si el email no tiene formato válido.
        """
        if len(username) < 3:
            raise ValueError(
                f"Username '{username}' debe tener al menos 3 caracteres."
            )
        if not username.isalnum():
            raise ValueError(
                f"Username '{username}' solo puede contener letras y números."
            )

        self._username: str = username
        self._email: Optional[str] = None
        self.email = email  # Usa el setter para validar
        self.nombre_completo: Optional[str] = nombre_completo
        self.activo: bool = True
        self.fecha_registro: datetime = datetime.now()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def username(self) -> str:
        """Username inmutable del usuario."""
        return self._username

    @property
    def email(self) -> str:
        """Correo electrónico validado del usuario."""
        return self._email  # type: ignore[return-value]

    @email.setter
    def email(self, valor: str) -> None:
        """Valida y asigna el email.

        Args:
            valor: Dirección de correo electrónico a validar.

        Raises:
            ValueError: Si el email no contiene '@' o '.'.
        """
        if "@" not in valor or "." not in valor:
            raise ValueError(
                f"Email inválido: '{valor}'. Debe contener '@' y '.'."
            )
        self._email = valor

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def activar(self) -> None:
        """Activa la cuenta del usuario."""
        self.activo = True

    def desactivar(self) -> None:
        """Desactiva la cuenta del usuario."""
        self.activo = False

    # ------------------------------------------------------------------
    # Métodos especiales
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Retorna la representación informal del usuario.

        Returns:
            String con el formato '@username'.
        """
        return f"@{self._username}"

    def __repr__(self) -> str:
        """Retorna la representación oficial del usuario.

        Returns:
            String con el formato "Usuario('username', 'email')".
        """
        return f"Usuario('{self._username}', '{self._email}')"
