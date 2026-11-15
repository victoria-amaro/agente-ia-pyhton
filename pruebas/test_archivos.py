from pathlib import Path

import pytest

from herramientas.archivos import guardar_markdown


def test_guarda_markdown_en_salida(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    resultado = guardar_markdown("guia_listas.md", "áéíóú")
    assert resultado["ok"] is True
    assert resultado["ruta"] == "salida/guia_listas.md"
    assert Path(resultado["ruta"]).read_text(encoding="utf-8") == "áéíóú"


@pytest.mark.parametrize(
    "nombre", ["guia.txt", "../guia.md", "/tmp/guia.md", "carpeta/guia.md", ""]
)
def test_rechaza_nombres_no_permitidos(tmp_path, monkeypatch, nombre):
    monkeypatch.chdir(tmp_path)
    resultado = guardar_markdown(nombre, "contenido")
    assert resultado["ok"] is False
    assert not (tmp_path.parent / "guia.md").exists()

