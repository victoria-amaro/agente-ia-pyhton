"""Interfaz síncrona y pequeña para ejecutar un agente de ADK."""

import os
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from runtime.errores import (
    ConfiguracionIncompleta,
    LimiteTemporal,
    ProveedorNoAdmitido,
    RespuestaVacia,
    ServicioNoDisponible,
)
from runtime.simulador import respuesta_simulada


APP_NAME = "learning_agents_python"
USER_ID = "estudiante"


def _validar_configuracion():
    proveedor = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if proveedor != "gemini":
        raise ProveedorNoAdmitido(
            "Esta versión admite solamente LLM_PROVIDER=gemini."
        )
    faltantes = [
        nombre
        for nombre in ("GOOGLE_API_KEY", "GEMINI_MODEL")
        if not os.getenv(nombre, "").strip()
    ]
    if faltantes:
        raise ConfiguracionIncompleta(
            "Falta configurar: " + ", ".join(faltantes) + "."
        )


def _clasificar_error(error):
    nombre = error.__class__.__name__.lower()
    codigo = getattr(error, "status_code", None) or getattr(error, "code", None)
    texto = str(error).lower()
    if codigo == 429 or "resourceexhausted" in nombre or "rate" in texto or "quota" in texto:
        return LimiteTemporal(
            "Se alcanzó un límite temporal o de cuota. Revisa los límites de la cuenta antes de volver a ejecutar."
        )
    if codigo in (500, 502, 503, 504) or any(
        marca in nombre or marca in texto
        for marca in ("serviceunavailable", "deadline", "timeout", "connection", "network")
    ):
        return ServicioNoDisponible(
            "El servicio no está disponible. Verifica la red o intenta más tarde."
        )
    return ServicioNoDisponible(
        "No fue posible comunicarse con el servicio del modelo."
    )


def ejecutar_agente(agente, mensaje, runner_factory=None):
    """Ejecuta una llamada y devuelve solamente el texto final."""
    if not isinstance(mensaje, str) or not mensaje.strip():
        raise ValueError("El mensaje no puede estar vacío.")

    if os.getenv("MODO_SIMULADO", "").strip() == "1":
        return respuesta_simulada(agente.name)

    _validar_configuracion()
    fabrica = runner_factory or Runner
    servicio = InMemorySessionService()
    runner = fabrica(
        app_name=APP_NAME,
        agent=agente,
        session_service=servicio,
        auto_create_session=True,
    )
    contenido = types.Content(
        role="user", parts=[types.Part.from_text(text=mensaje.strip())]
    )
    respuesta = ""
    try:
        eventos = runner.run(
            user_id=USER_ID,
            session_id=str(uuid.uuid4()),
            new_message=contenido,
        )
        for evento in eventos:
            if not evento.is_final_response() or not evento.content:
                continue
            partes = evento.content.parts or []
            textos = [parte.text for parte in partes if getattr(parte, "text", None)]
            if textos:
                respuesta = "".join(textos).strip()
    except (ConfiguracionIncompleta, ProveedorNoAdmitido, RespuestaVacia):
        raise
    except Exception as error:
        raise _clasificar_error(error) from error

    if not respuesta:
        raise RespuestaVacia("El agente terminó sin producir una respuesta de texto.")
    return respuesta
