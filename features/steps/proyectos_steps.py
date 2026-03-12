# -*- coding: utf-8 -*-
"""Steps BDD para los escenarios de proyectos."""

from behave import given, when, then

from src.domain.enums import PrioridadTarea
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.usuario import Usuario

_PRIORIDADES = {
    "ALTA": PrioridadTarea.ALTA,
    "MEDIA": PrioridadTarea.MEDIA,
    "BAJA": PrioridadTarea.BAJA,
}


@given('que existe un proyecto "{nombre}" liderado por ese usuario')
def step_crear_proyecto(context, nombre):
    context.proyecto = Proyecto(nombre=nombre, lider=context.usuario)
    context.tareas_proyecto = []


@given('que existe una tarea "{titulo}" con prioridad {prioridad}')
def step_crear_tarea_proyecto(context, titulo, prioridad):
    nueva = Tarea(titulo=titulo, prioridad=_PRIORIDADES[prioridad])
    context.tareas_proyecto.append(nueva)
    context.tarea = nueva


@when("se agrega la tarea al proyecto")
def step_agregar_tarea(context):
    try:
        context.proyecto.agregar_tarea(context.tarea)
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@when("se intenta agregar la misma tarea de nuevo")
def step_agregar_tarea_duplicada(context):
    try:
        context.proyecto.agregar_tarea(context.tarea)
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@when("se agregan ambas tareas al proyecto")
def step_agregar_ambas_tareas(context):
    for t in context.tareas_proyecto:
        context.proyecto.agregar_tarea(t)


@when('se intenta crear un proyecto con nombre "{nombre}"')
def step_intentar_crear_proyecto(context, nombre):
    try:
        context.proyecto = Proyecto(nombre=nombre, lider=context.usuario)
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@then("el proyecto tiene {cantidad:d} tarea")
def step_verificar_cantidad_tareas(context, cantidad):
    assert len(context.proyecto.tareas) == cantidad, (
        f"Se esperaban {cantidad} tareas, se obtuvo {len(context.proyecto.tareas)}"
    )


@then("filtrar por prioridad {prioridad} retorna {cantidad:d} tarea")
def step_filtrar_por_prioridad(context, prioridad, cantidad):
    tareas = context.proyecto.obtener_tareas_por_prioridad(_PRIORIDADES[prioridad])
    assert len(tareas) == cantidad, (
        f"Se esperaban {cantidad} tareas con prioridad {prioridad}, se obtuvo {len(tareas)}"
    )
