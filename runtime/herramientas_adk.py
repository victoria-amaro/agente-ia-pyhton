"""Adaptadores tipados requeridos por ADK; no requieren cambios."""

from google.adk.tools import FunctionTool

from herramientas.archivos import guardar_markdown
from herramientas.validacion import validar_guia


def guardar_markdown_adk(nombre_archivo: str, contenido: str) -> dict:
    """Guarda contenido Markdown de forma segura dentro de salida/."""
    return guardar_markdown(nombre_archivo, contenido)


def validar_guia_adk(contenido: str) -> dict:
    """Comprueba que una guía tenga la estructura obligatoria."""
    return validar_guia(contenido)


herramienta_guardar_markdown = FunctionTool(func=guardar_markdown_adk)
herramienta_validar_guia = FunctionTool(func=validar_guia_adk)

