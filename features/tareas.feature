# language: es
Característica: Gestión de tareas
  Como sistema TaskFlow
  Quiero gestionar el ciclo de vida de las tareas correctamente
  Para controlar el progreso del trabajo

  Antecedentes:
    Dado que existe una tarea pendiente con título "Tarea base" y prioridad MEDIA

  Escenario: Completar una tarea exitosamente
    Cuando se completa la tarea
    Entonces la tarea tiene estado COMPLETADA
    Y la tarea tiene fecha de completado registrada

  Escenario: Completar una tarea ya completada lanza error
    Dado que la tarea ya fue completada
    Cuando se intenta completar la tarea de nuevo
    Entonces se produce un error con mensaje "ya está completada"

  Escenario: Cambiar prioridad de una tarea
    Cuando se cambia la prioridad de la tarea a ALTA
    Entonces la tarea tiene prioridad ALTA

  Esquema del escenario: Título de tarea inválido lanza error
    Cuando se intenta crear una tarea con título "<titulo>"
    Entonces se produce un error con mensaje "<fragmento>"

    Ejemplos:
      | titulo | fragmento             |
      | AB     | al menos 3 caracteres |
      | z      | al menos 3 caracteres |
