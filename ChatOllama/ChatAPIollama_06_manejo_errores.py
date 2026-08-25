"""
PASO 6: Controlar errores sin cerrar inesperadamente el chat.

Roadmap:
1. ChatAPIollama_01_pregunta_fija.py: enviar una pregunta fija.
2. ChatAPIollama_02_pregunta_usuario.py: escribir una pregunta.
3. ChatAPIollama_03_chat_continuo.py: conversar y conservar el historial.
4. ChatAPIollama_04_chat_streaming.py: mostrar respuestas en tiempo real.
5. ChatAPIollama_05_historial_json.py: guardar el historial en JSON.
6. Este archivo: detectar y explicar los errores más comunes.
"""

# Importa json para leer y guardar el historial.
import json

# Importa Path para construir la ruta del archivo JSON.
from pathlib import Path

# Importa los errores de conexión que puede producir la API.
import httpx  # pyright: ignore[reportMissingImports]

# Importa la librería que permite comunicarse con Ollama.
import ollama  # pyright: ignore[reportMissingImports]


# Usa un JSON propio para no mezclarlo con el historial del ejemplo 5.
ARCHIVO_HISTORIAL = Path(__file__).with_name("historial_conversacion_06.json")

# Define el comportamiento inicial del asistente.
MENSAJE_SISTEMA = {
    "role": "system",
    "content": "Eres un asistente amable y respondes de forma clara."
}


def cargar_historial():
    """Carga los mensajes del JSON o crea una conversación nueva."""

    # Si el archivo todavía no existe, devuelve el mensaje inicial.
    if not ARCHIVO_HISTORIAL.exists():
        return [MENSAJE_SISTEMA]

    try:
        # Abre y convierte el JSON en una lista de Python.
        with ARCHIVO_HISTORIAL.open("r", encoding="utf-8") as archivo:
            mensajes_guardados = json.load(archivo)

        # Comprueba que el contenido tenga el tipo esperado.
        if not isinstance(mensajes_guardados, list):
            raise ValueError("El historial no contiene una lista.")

        print(f"Se cargaron {len(mensajes_guardados)} mensajes del historial.")
        return mensajes_guardados

    # Controla archivos dañados, contenido incorrecto o errores de lectura.
    except json.JSONDecodeError:
        print("El historial contiene JSON inválido. Se iniciará uno nuevo.")
    except OSError as error:
        print(f"No fue posible leer el historial: {error}")
    except ValueError as error:
        print(f"El historial no tiene el formato esperado: {error}")

    return [MENSAJE_SISTEMA]


def guardar_historial(mensajes):
    """Guarda los mensajes y controla posibles errores de escritura."""

    try:
        # Abre el archivo en modo escritura y guarda la conversación.
        with ARCHIVO_HISTORIAL.open("w", encoding="utf-8") as archivo:
            json.dump(mensajes, archivo, ensure_ascii=False, indent=4)

        print(f"Historial guardado en: {ARCHIVO_HISTORIAL.name}")

    # Evita que el chat se cierre si el archivo no se puede guardar.
    except OSError as error:
        print(f"Aviso: no fue posible guardar el historial: {error}")


# Recupera el historial antes de iniciar el chat.
mensajes = cargar_historial()

# Muestra las instrucciones iniciales.
print("Chat con Ollama (manejo de errores)")
print("Escribe 'salir' para terminar.")

# Mantiene el chat activo hasta que el usuario decida terminar.
while True:
    try:
        # Solicita un mensaje y elimina espacios innecesarios.
        pregunta = input("\nTú: ").strip()

    # Permite cerrar ordenadamente con Ctrl + C o con el fin de la entrada.
    except (KeyboardInterrupt, EOFError):
        print("\nChat: Programa cerrado por el usuario.")
        break

    # Termina normalmente cuando el usuario escribe "salir".
    if pregunta.lower() == "salir":
        print("Chat: Hasta luego.")
        break

    # Ignora los mensajes vacíos.
    if not pregunta:
        continue

    # Agrega la pregunta al historial en memoria.
    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    # Guarda temporalmente los fragmentos de la respuesta.
    texto_respuesta = ""

    try:
        # Solicita a Ollama una respuesta en tiempo real.
        respuesta_stream = ollama.chat(
            model="llama3.2:latest",
            messages=mensajes,
            options={
                "temperature": 0.3
            },
            stream=True
        )

        print("\nChat: ", end="", flush=True)

        # Imprime y une cada fragmento generado por Ollama.
        for fragmento in respuesta_stream:
            texto_fragmento = fragmento["message"]["content"]
            print(texto_fragmento, end="", flush=True)
            texto_respuesta += texto_fragmento

        print()

    # Controla errores enviados por Ollama, como un modelo inexistente.
    except ollama.ResponseError as error:
        mensajes.pop()
        print(f"\nError de Ollama: {error}")
        if error.status_code == 404:
            print("Verifica que el modelo esté instalado con: ollama list")
        continue

    # Controla cuando Ollama está cerrado o no acepta conexiones.
    except httpx.ConnectError:
        mensajes.pop()
        print("\nNo fue posible conectarse con Ollama.")
        print("Abre Ollama o ejecuta: ollama serve")
        continue

    # Controla cuando Ollama tarda demasiado en responder.
    except httpx.TimeoutException:
        mensajes.pop()
        print("\nOllama tardó demasiado en responder. Inténtalo nuevamente.")
        continue

    # Controla cualquier otro error inesperado sin ocultar su descripción.
    except Exception as error:
        mensajes.pop()
        print(f"\nOcurrió un error inesperado: {error}")
        continue

    # Agrega la respuesta completa solamente si terminó correctamente.
    mensajes.append(
        {
            "role": "assistant",
            "content": texto_respuesta
        }
    )

    # Guarda en JSON la pregunta y su respuesta.
    guardar_historial(mensajes)
