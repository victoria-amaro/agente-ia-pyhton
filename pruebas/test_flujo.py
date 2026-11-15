from pathlib import Path

import pytest

import main


@pytest.fixture(autouse=True)
def modelo_de_prueba(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "modelo-local-para-pruebas")


def test_flujo_simulado_realiza_tres_llamadas_y_guarda(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    llamadas = []

    def ejecutar_falso(agente, mensaje):
        llamadas.append((agente.name, mensaje))
        if agente.name == "explicador_python":
            return "## Explicación\n\nTexto.\n\n```python\nprint(1)\n```"
        if agente.name == "disenador_practica":
            return "## Práctica\n\nEjercicio con tres criterios."
        return """# Guía de estudio: listas

## Explicación

Texto.

```python
print(1)
```

## Práctica

Ejercicio con tres criterios.

## Revisión

No se requirieron cambios importantes.
"""

    resultado = main.ejecutar_flujo("listas", ejecutar=ejecutar_falso)
    assert len(llamadas) == 3
    assert llamadas[0][0] == "explicador_python"
    assert "Texto.\n\n```python\nprint(1)\n```" in llamadas[1][1]
    assert "# Guía de estudio: listas" in llamadas[2][1]
    assert Path(resultado["ruta"]).exists()


def test_flujo_rechaza_tema_vacio():
    with pytest.raises(ValueError, match="vacío"):
        main.ejecutar_flujo("   ", ejecutar=lambda agente, mensaje: "no usado")


def test_extension_hace_una_sola_correccion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    llamadas = []

    def ejecutar_falso(agente, mensaje):
        llamadas.append((agente.name, mensaje))
        if len(llamadas) == 1:
            return "## Explicación\nTexto sin código."
        if len(llamadas) == 2:
            return "## Práctica\nEjercicio."
        if len(llamadas) == 3:
            return "guía incompleta"
        return """# Guía de estudio: listas
## Explicación
```python
print(1)
```
## Práctica
Ejercicio.
## Revisión
Corregida.
"""

    resultado = main.ejecutar_flujo(
        "listas", ejecutar=ejecutar_falso, permitir_correccion=True
    )
    assert resultado["ok"] is True
    assert len(llamadas) == 4
    assert "guía incompleta" in llamadas[3][1]
    assert "## Revisión" in llamadas[3][1]
