# -*- coding: utf-8 -*-
"""Configuración de behave: hooks de ciclo de vida de los escenarios."""


def before_scenario(context, scenario):
    """Limpia el contexto antes de cada escenario."""
    context.usuario = None
    context.proyecto = None
    context.tarea = None
    context.tareas_proyecto = []
    context.ultimo_error = None
    context.resultado = None
