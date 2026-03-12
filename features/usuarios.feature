# language: es
Característica: Gestión de usuarios
  Como sistema TaskFlow
  Quiero gestionar usuarios correctamente
  Para asegurar la integridad de los datos

  Antecedentes:
    Dado que existe un usuario válido con username "testuser" y email "test@example.com"

  Escenario: Crear usuario válido exitosamente
    Entonces el usuario tiene username "testuser"
    Y el usuario tiene email "test@example.com"
    Y el usuario está activo

  Escenario: Desactivar y activar un usuario
    Cuando se desactiva el usuario
    Entonces el usuario no está activo
    Cuando se activa el usuario
    Entonces el usuario está activo

  Esquema del escenario: Username inválido lanza error
    Cuando se intenta crear un usuario con username "<username>" y email "ok@test.com"
    Entonces se produce un error con mensaje "<fragmento>"

    Ejemplos:
      | username   | fragmento              |
      | ab         | al menos 3 caracteres  |
      | x          | al menos 3 caracteres  |
      | user@name  | solo puede contener    |
      | user.name  | solo puede contener    |

  Escenario: Email inválido lanza error
    Cuando se intenta crear un usuario con username "valido" y email "emailinvalido"
    Entonces se produce un error con mensaje "Email inválido"
