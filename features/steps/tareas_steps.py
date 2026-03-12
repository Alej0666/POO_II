# -*- coding: utf-8 -*-
"""Steps BDD para los escenarios de tareas."""

from behave import given, when, then
from datetime import datetime

from src.domain.enums import EstadoTarea, PrioridadTarea
from src.domain.tarea import Tarea

_PRIORIDADES = {
    "ALTA": PrioridadTarea.ALTA,
    "MEDIA": PrioridadTarea.MEDIA,
    "BAJA": PrioridadTarea.BAJA,
}

_ESTADOS = {
    "PENDIENTE": EstadoTarea.PENDIENTE,
    "EN_PROGRESO": EstadoTarea.EN_PROGRESO,
    "COMPLETADA": EstadoTarea.COMPLETADA,
}


@given('que existe una tarea pendiente con título "{titulo}" y prioridad {prioridad}')
def step_crear_tarea_pendiente(context, titulo, prioridad):
    context.tarea = Tarea(titulo=titulo, prioridad=_PRIORIDADES[prioridad])


@given("que la tarea ya fue completada")
def step_tarea_ya_completada(context):
    context.tarea.completar()


@when("se completa la tarea")
def step_completar_tarea(context):
    try:
        context.tarea.completar()
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@when("se intenta completar la tarea de nuevo")
def step_intentar_completar_de_nuevo(context):
    try:
        context.tarea.completar()
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@when("se cambia la prioridad de la tarea a {prioridad}")
def step_cambiar_prioridad(context, prioridad):
    context.tarea.cambiar_prioridad(_PRIORIDADES[prioridad])


@when('se intenta crear una tarea con título "{titulo}"')
def step_intentar_crear_tarea(context, titulo):
    try:
        context.tarea = Tarea(titulo=titulo, prioridad=PrioridadTarea.MEDIA)
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@then("la tarea tiene estado {estado}")
def step_verificar_estado(context, estado):
    assert context.tarea.estado == _ESTADOS[estado], (
        f"Se esperaba estado {estado}, se obtuvo {context.tarea.estado}"
    )


@then("la tarea tiene fecha de completado registrada")
def step_verificar_fecha_completado(context):
    assert isinstance(context.tarea.fecha_completado, datetime), (
        "Se esperaba una fecha de completado pero es None"
    )


@then("la tarea tiene prioridad {prioridad}")
def step_verificar_prioridad(context, prioridad):
    assert context.tarea.prioridad == _PRIORIDADES[prioridad], (
        f"Se esperaba prioridad {prioridad}, se obtuvo {context.tarea.prioridad}"
    )
