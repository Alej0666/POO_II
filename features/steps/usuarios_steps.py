# -*- coding: utf-8 -*-
"""Steps BDD para los escenarios de usuarios."""

from behave import given, when, then

from src.domain.usuario import Usuario


@given('que existe un usuario válido con username "{username}" y email "{email}"')
def step_crear_usuario_valido(context, username, email):
    context.usuario = Usuario(username=username, email=email)


@when('se intenta crear un usuario con username "{username}" y email "{email}"')
def step_intentar_crear_usuario(context, username, email):
    try:
        context.usuario = Usuario(username=username, email=email)
        context.ultimo_error = None
    except ValueError as e:
        context.ultimo_error = str(e)


@when("se desactiva el usuario")
def step_desactivar_usuario(context):
    context.usuario.desactivar()


@when("se activa el usuario")
def step_activar_usuario(context):
    context.usuario.activar()


@then('el usuario tiene username "{username}"')
def step_verificar_username(context, username):
    assert context.usuario.username == username, (
        f"Se esperaba '{username}', se obtuvo '{context.usuario.username}'"
    )


@then('el usuario tiene email "{email}"')
def step_verificar_email(context, email):
    assert context.usuario.email == email, (
        f"Se esperaba '{email}', se obtuvo '{context.usuario.email}'"
    )


@then("el usuario está activo")
def step_usuario_activo(context):
    assert context.usuario.activo is True, "Se esperaba que el usuario estuviera activo"


@then("el usuario no está activo")
def step_usuario_inactivo(context):
    assert context.usuario.activo is False, "Se esperaba que el usuario estuviera inactivo"


@then('se produce un error con mensaje "{fragmento}"')
def step_verificar_error(context, fragmento):
    assert context.ultimo_error is not None, "Se esperaba un error pero no se produjo ninguno"
    assert fragmento in context.ultimo_error, (
        f"Se esperaba '{fragmento}' en el error, pero se obtuvo: '{context.ultimo_error}'"
    )
