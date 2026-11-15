"""Agente explicador. Completa este archivo en la tarea correspondiente."""
import os 
from google.adk.agents import Agent

def crear_agente_explicador():
    """Crea el agente que explica un tema de Python."""
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    descripcion = "Agente de Python que explica conceptos y ejemplos de código de manera sencilla" 
    instrucciones = """ 
            Eres un agente de IA que ayuda al usuario a comprender conceptos de Python. 
            Tus funciones son: 
            1.Proporciona explicaciones claras y ejemplos de código cuando sea necesario. 
            2.También contestas dudas puntuales de los usuarios. 
            3.Si no sabes algo o no estas seguro, no das información. 
            4.Le pedis al usuario que desarrolle mejor para ver si se puede ayudar. 
            5.Responde siempre en español e incluye tres partes:
                1. Una explicación breve y clara del tema.
                2. Un ejemplo pequeño y funcional de código en Python.
                3. Un error frecuente o advertencia sobre ese tema.
            """
    return Agent(
            name="explicador_python",
            model=modelo,
            description=descripcion,
            instruction=instrucciones,
        )