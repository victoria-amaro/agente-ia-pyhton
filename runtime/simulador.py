"""Respuestas fijas para contingencia y pruebas sin consumo de API."""

import json
from pathlib import Path


RUTA_RESPUESTAS = Path(__file__).resolve().parents[1] / "ejemplos" / "respuestas_simuladas.json"


def respuesta_simulada(nombre_agente):
    """Devuelve la respuesta fija asociada al nombre del agente."""
    datos = json.loads(RUTA_RESPUESTAS.read_text(encoding="utf-8"))
    try:
        return datos[nombre_agente]
    except KeyError as error:
        raise ValueError("No existe una respuesta simulada para ese agente") from error

