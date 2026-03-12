# language: es
Característica: Gestión de proyectos
  Como sistema TaskFlow
  Quiero gestionar proyectos y sus tareas correctamente
  Para organizar el trabajo del equipo

  Antecedentes:
    Dado que existe un usuario válido con username "lider01" y email "lider@test.com"
    Y que existe un proyecto "Proyecto Alpha" liderado por ese usuario

  Escenario: Agregar tarea al proyecto exitosamente
    Dado que existe una tarea "Implementar módulo" con prioridad ALTA
    Cuando se agrega la tarea al proyecto
    Entonces el proyecto tiene 1 tarea

  Escenario: Agregar tarea duplicada lanza error
    Dado que existe una tarea "Tarea duplicada" con prioridad MEDIA
    Cuando se agrega la tarea al proyecto
    Y se intenta agregar la misma tarea de nuevo
    Entonces se produce un error con mensaje "ya existe en el proyecto"

  Escenario: Filtrar tareas por prioridad
    Dado que existe una tarea "Tarea prioritaria" con prioridad ALTA
    Y que existe una tarea "Tarea secundaria" con prioridad BAJA
    Cuando se agregan ambas tareas al proyecto
    Entonces filtrar por prioridad ALTA retorna 1 tarea
    Y filtrar por prioridad BAJA retorna 1 tarea

  Esquema del escenario: Nombre de proyecto inválido lanza error
    Cuando se intenta crear un proyecto con nombre "<nombre>"
    Entonces se produce un error con mensaje "<fragmento>"

    Ejemplos:
      | nombre | fragmento             |
      | AB     | al menos 3 caracteres |
      | X      | al menos 3 caracteres |
