from types import SimpleNamespace

import pytest

from runtime.ejecutor import ejecutar_agente
from runtime.errores import LimiteTemporal, RespuestaVacia, ServicioNoDisponible


class Evento:
    def __init__(self, texto):
        self.content = SimpleNamespace(parts=[SimpleNamespace(text=texto)])

    def is_final_response(self):
        return True


def fabrica_con_eventos(eventos):
    class RunnerFalso:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def run(self, **kwargs):
            return iter(eventos)

    return RunnerFalso


def configurar(monkeypatch):
    monkeypatch.delenv("MODO_SIMULADO", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GOOGLE_API_KEY", "valor-solo-para-prueba")
    monkeypatch.setenv("GEMINI_MODEL", "modelo-de-prueba")


def test_ejecutor_devuelve_texto_final(monkeypatch):
    configurar(monkeypatch)
    agente = SimpleNamespace(name="agente_prueba")
    respuesta = ejecutar_agente(
        agente, "mensaje", runner_factory=fabrica_con_eventos([Evento("respuesta")])
    )
    assert respuesta == "respuesta"


def test_ejecutor_rechaza_respuesta_vacia(monkeypatch):
    configurar(monkeypatch)
    agente = SimpleNamespace(name="agente_prueba")
    with pytest.raises(RespuestaVacia):
        ejecutar_agente(
            agente, "mensaje", runner_factory=fabrica_con_eventos([Evento("")])
        )


@pytest.mark.parametrize(
    ("mensaje", "tipo"),
    [("429 quota exceeded", LimiteTemporal), ("connection timeout", ServicioNoDisponible)],
)
def test_ejecutor_normaliza_errores(monkeypatch, mensaje, tipo):
    configurar(monkeypatch)

    class RunnerFalso:
        def __init__(self, **kwargs):
            pass

        def run(self, **kwargs):
            raise RuntimeError(mensaje)

    with pytest.raises(tipo):
        ejecutar_agente(SimpleNamespace(name="agente_prueba"), "mensaje", RunnerFalso)

