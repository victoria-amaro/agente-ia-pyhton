import os

import pytest

from herramientas.validacion import validar_guia


GUIA_VALIDA = """# Guía de estudio: Listas

## Explicación

Texto breve.

```python
print([1, 2])
```

## Práctica

Ejercicio.

## Revisión

No se requirieron cambios importantes.
"""


def test_acepta_guia_completa(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    assert validar_guia(GUIA_VALIDA) == {"valida": True, "faltantes": []}


@pytest.mark.parametrize(
    ("contenido", "faltante"),
    [
        ("", "contenido no vacío"),
        (GUIA_VALIDA.replace("# Guía de estudio:", "# Apuntes:"), "título"),
        (GUIA_VALIDA.replace("## Práctica", "## Ejercicio"), "## Práctica"),
        (GUIA_VALIDA.replace("```python", "```text"), "bloque de código Python"),
    ],
)
def test_informa_requisito_faltante(monkeypatch, contenido, faltante):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    resultado = validar_guia(contenido)
    assert resultado["valida"] is False
    assert faltante in resultado["faltantes"]


def test_detecta_clave_configurada(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "clave-simulada-123456")
    resultado = validar_guia(GUIA_VALIDA + os.environ["GOOGLE_API_KEY"])
    assert "contenido sensible" in resultado["faltantes"]

