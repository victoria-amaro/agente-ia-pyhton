import importlib.metadata
import inspect
from pathlib import Path

import main


RAIZ = Path(__file__).resolve().parents[1]


def test_estructura_minima_del_starter_pack():
    requeridos = [
        "agentes/explicador.py",
        "agentes/disenador_practica.py",
        "agentes/revisor.py",
        "herramientas/archivos.py",
        "herramientas/validacion.py",
        "runtime/ejecutor.py",
        "runtime/herramientas_adk.py",
        "runtime/errores.py",
        "salida/.gitkeep",
        ".env.example",
        ".gitignore",
        "main.py",
        "README.md",
    ]
    assert all((RAIZ / ruta).exists() for ruta in requeridos)


def test_version_de_adk_fijada():
    assert importlib.metadata.version("google-adk") == "2.8.0"


def test_env_no_se_confirma_en_git():
    gitignore = (RAIZ / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in gitignore


def test_readme_documenta_comandos_de_ejecucion():
    instrucciones = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "docker pull" in instrucciones
    assert "docker run" in instrucciones
    assert "--env-file .env" in instrucciones


def test_firma_del_flujo_permite_sustituir_el_ejecutor():
    parametros = inspect.signature(main.ejecutar_flujo).parameters
    assert list(parametros) == ["tema", "ejecutar", "permitir_correccion"]
    assert callable(parametros["ejecutar"].default)
    assert parametros["permitir_correccion"].default is False
