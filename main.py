"""Aplicación principal. Completa el flujo en la tarea de integración."""

from runtime.ejecutor import ejecutar_agente


def ejecutar_flujo(tema, ejecutar=ejecutar_agente, permitir_correccion=False):
    """Coordina los agentes usando un ejecutor reemplazable en las pruebas."""
    raise NotImplementedError("Completa ejecutar_flujo")


def main():
    tema = input("Tema de Python: ").strip()
    if not tema:
        print("El tema no puede estar vacío.")
        return 1
    ejecutar_flujo(tema)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
