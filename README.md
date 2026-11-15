# Objetivo del proyecto:

El objetivo es generar guías de estudio de Python coordinando tres agentes: uno que explica el tema, otro que propone una práctica y un tercero que revisa el borrador, validando

# Agentes de IA con Python

Documentación de la aplicación. Amplía este README, situado junto a `main.py`,
con las decisiones, los ejemplos y la reflexión del proyecto.

La imagen creó estos archivos con `iniciar-proyecto`. Consulta la
[guía de trabajo con Docker y VS Code](docs/trabajar-con-docker.md).

## Antes de comenzar

La imagen Docker proporcionada contiene Python, ADK y las dependencias necesarias.

Configura la imagen pública preparada para este proyecto una vez en cada
terminal y descárgala:

```bash
export AGENTS_IMAGE="ghcr.io/hbtn-edu/ai-agents-python:0.4.0"
docker pull "$AGENTS_IMAGE"
```

Ubícate en la carpeta local creada al inicializar el proyecto. `"$PWD"` comparte la carpeta
actual con el contenedor para que puedas editarla con tus herramientas habituales.

```bash
# Comprobar Python, ADK y el entorno sin consumir API
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m runtime.diagnostico --sin-api

# Ejecutar las pruebas básicas del starter pack
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" \
  python -m pytest -q pruebas/test_entorno.py pruebas/test_runtime.py

# Ejecutar todas las pruebas públicas de las tareas obligatorias durante el proyecto
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m pytest -q -k 'not extension'

# Ejecutar la aplicación después de configurar .env
docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python main.py
```

La prueba de la extensión opcional se ejecuta con `python -m pytest -q pruebas/test_flujo.py`,
usando el mismo comando Docker y sin el filtro `-k`.

Las pruebas de agentes, archivos, validación y flujo fallan al comienzo porque
corresponden al trabajo que debes completar. Las pruebas de entorno y runtime
deben pasar desde el primer momento.

## Configuración segura de Gemini

1. Abre [Google AI Studio](https://aistudio.google.com/apikey) e inicia sesión.
2. Crea una clave en la sección de claves de API. Si la cuenta requiere asociar
   un proyecto de Google Cloud, sigue la
   [guía de creación y gestión de claves](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419).
3. Edita el `.env` creado al inicializar y completa `GOOGLE_API_KEY` con la clave.
4. Conserva `GEMINI_MODEL=gemini-3.5-flash` y las demás variables del archivo.
5. Comprueba con `git check-ignore .env` que Git ignora el archivo.

```bash
git check-ignore .env

docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m runtime.diagnostico --sin-api
```

La siguiente comprobación realiza una llamada real y consume cuota. Ejecútala
una vez para verificar el acceso:

```bash
docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m runtime.diagnostico --con-api
```

El diagnóstico informa si la clave está configurada, pero nunca muestra su
valor ni una parte de ella.

### Si el servicio no está disponible

El modelo configurado es `gemini-3.5-flash`, probado con este starter pack.
Si aparece `503 UNAVAILABLE` o «El servicio no está disponible», termina esa
ejecución, espera al menos un minuto y vuelve a ejecutar manualmente el mismo
comando una sola vez. Si vuelve a fallar, registra el modelo, la hora y el
mensaje, y consulta el [estado del servicio](https://aistudio.google.com/status).
Mientras se restablece, el modo simulado permite comprobar las operaciones locales.

Ante un error de cuota (`429`), detén las llamadas y revisa los límites de la
cuenta antes de una nueva ejecución. Consulta la
[guía de solución de problemas](https://ai.google.dev/gemini-api/docs/troubleshooting?hl=es-419),
solamente «Estrategia de reintentos» y «Verifica si tienes el modelo correcto».

## Modo simulado

Las respuestas fijas incluidas permiten comprobar el flujo sin consumir API.
La calidad de las respuestas a temas diferentes se verifica con ejecuciones reales.

```bash
docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -e MODO_SIMULADO=1 \
  -v "$PWD:/workspace" -w /workspace "$AGENTS_IMAGE" python main.py
```

## Estructura

- `agentes/`: archivos que completarás para cada agente.
- `herramientas/`: guardado seguro y validación determinista.
- `runtime/`: infraestructura de ejecución suministrada.
- `pruebas/`: pruebas públicas que no consumen API.
- `ejemplos/`: respuestas fijas y guías de ejemplo.
- `salida/`: archivos generados, ignorados por Git.

## Recomendaciones de seguridad y privacidad

- Utiliza datos ficticios y limita el contexto enviado a la información necesaria.
- Mantén la clave en `.env`, excluida de Git, documentación, capturas y mensajes.
- Si una clave se expone, revócala y reemplázala.
