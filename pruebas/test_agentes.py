import pytest

from agentes.disenador_practica import crear_agente_disenador
from agentes.explicador import crear_agente_explicador
from agentes.revisor import crear_agente_revisor


@pytest.fixture(autouse=True)
def modelo_de_prueba(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "modelo-local-para-pruebas")


def test_explicador_define_identidad_y_formato():
    agente = crear_agente_explicador()
    assert agente.instruction.strip()
    assert agente.name == "explicador_python"
    assert agente.model
    assert agente.description


def test_disenador_usa_contexto_y_criterios():
    agente = crear_agente_disenador()
    assert agente.instruction.strip()
    assert agente.name == "disenador_practica"
    assert agente.model
    assert agente.description


def test_revisor_devuelve_una_guia_completa():
    agente = crear_agente_revisor()
    assert agente.instruction.strip()
    assert agente.name == "revisor_python"
    assert agente.model
    assert agente.description
