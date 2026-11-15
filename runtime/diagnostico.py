"""Comprobaciones del entorno con y sin una llamada real a Gemini."""

import argparse
import importlib.metadata
import os
import sys


def comprobar_sin_api():
    proveedor = os.getenv("LLM_PROVIDER", "gemini")
    modelo = os.getenv("GEMINI_MODEL", "")
    clave_configurada = bool(os.getenv("GOOGLE_API_KEY", "").strip())
    print(f"Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"google-adk: {importlib.metadata.version('google-adk')}")
    print(f"Proveedor: {proveedor}")
    print(f"Modelo configurado: {'sí' if modelo else 'no'}")
    print(f"Clave configurada: {'sí' if clave_configurada else 'no'}")
    print("Entorno básico: correcto")


def comprobar_con_api():
    from google.adk.agents import Agent

    from runtime.ejecutor import ejecutar_agente

    modelo = os.getenv("GEMINI_MODEL", "")
    agente = Agent(
        name="diagnostico",
        model=modelo,
        description="Comprueba la conexión.",
        instruction="Responde solamente: conexión correcta",
    )
    respuesta = ejecutar_agente(agente, "Comprueba la conexión")
    print("Consulta a Gemini: correcta" if respuesta else "Consulta a Gemini: sin respuesta")


def main():
    parser = argparse.ArgumentParser(description="Diagnóstico del starter pack")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--sin-api", action="store_true")
    grupo.add_argument("--con-api", action="store_true")
    opciones = parser.parse_args()
    comprobar_sin_api()
    if opciones.con_api:
        comprobar_con_api()


if __name__ == "__main__":
    main()

