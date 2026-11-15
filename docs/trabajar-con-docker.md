# Trabajar con la imagen Docker

La imagen contiene Python, las dependencias, las pruebas y los archivos iniciales.
`iniciar-proyecto` copia esos archivos a una carpeta local vacía.

## Crear el espacio de trabajo

En una terminal de tu equipo (Linux, macOS o WSL), ejecuta:

```bash
mkdir mi-proyecto-agentes
cd mi-proyecto-agentes
export AGENTS_IMAGE="ghcr.io/hbtn-edu/ai-agents-python:0.4.0"
docker pull "$AGENTS_IMAGE"
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/workspace" "$AGENTS_IMAGE" iniciar-proyecto
git init
```

El nombre de carpeta es un ejemplo. La inicialización requiere una carpeta vacía;
si contiene archivos, se detiene sin modificarlos. Crea también `.env`
con la clave vacía, excluido por `.gitignore`.

## Editar y ejecutar

Abre la carpeta local con tu editor. El `README.md` situado junto a
`main.py` es la documentación de tu aplicación: amplíalo conservando
los comandos de configuración y ejecución.

Ejecuta los comandos Docker desde esa carpeta. `-v "$PWD:/workspace"`
comparte la carpeta con el contenedor; `-w /workspace` selecciona
el directorio de ejecución. `--user` conserva permisos compatibles
con tu usuario local. `--rm` elimina el contenedor al terminar;
los archivos de la carpeta compartida permanecen en tu equipo.

```bash
docker run --rm -it --user "$(id -u):$(id -g)" \
  -v "$PWD:/workspace" -w /workspace "$AGENTS_IMAGE" \
  python -m runtime.diagnostico --sin-api
```

Las ejecuciones con configuración agregan `--env-file .env`
antes de la imagen. En cada terminal nueva vuelve a definir `AGENTS_IMAGE`.
Tras guardar cambios con el editor, vuelve a ejecutar la prueba o la aplicación.

En Windows usa una terminal WSL con integración de Docker Desktop. Si Docker
informa que no puede compartir la carpeta, revisa el acceso de Docker Desktop
a la ubicación seleccionada.

## VS Code dentro del contenedor (opcional)

1. Inicializa la carpeta. Instala Visual Studio Code y la extensión oficial
   **Dev Containers** de Microsoft.
2. Abre la carpeta local en VS Code. Incluye `.devcontainer/devcontainer.json`,
   que selecciona la imagen y monta la carpeta en `/workspace`.
3. En la paleta de comandos selecciona **Dev Containers: Reopen in Container**.
   Espera la conexión; la primera apertura necesita Internet para los componentes
   de edición. En Linux la configuración ajusta el usuario remoto al usuario local.
4. Abre **Terminal → New Terminal**. Ejecuta `pwd`: debe mostrar
   `/workspace`. Allí puedes probar directamente:

```bash
python -m runtime.diagnostico --sin-api
python -m pytest -q pruebas/test_entorno.py pruebas/test_runtime.py
```

El prefijo `docker run ...` de las tareas corresponde a la terminal
de tu equipo. Los comandos Git también se ejecutan en la terminal local.
En la terminal conectada de VS Code utiliza solamente la parte
`python ...`. Después de completar el flujo, el modo simulado se ejecuta así:

```bash
MODO_SIMULADO=1 python main.py
```

Edita los mismos archivos desde el explorador de VS Code; quedan guardados en
tu carpeta local. Para volver al editor local selecciona
**Dev Containers: Reopen Folder Locally**.

El contenedor carga `.env` al crearse. Después de modificar la clave
o el modelo, guarda el archivo y usa **Dev Containers: Rebuild Container**.
Abrir otra terminal no recarga esas variables. Evita imprimir la clave o copiarla
a la configuración de VS Code.

Referencia: [documentación oficial de Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).
Consulta «Open an existing folder in a container» y «Opening a terminal»;
la configuración de este proyecto ya está incluida.
