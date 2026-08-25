"""
PASO 5: Guardar y recuperar el contexto de la conversación en JSON.

Roadmap:
1. ChatAPIollama_01_pregunta_fija.py: enviar una pregunta fija.
2. ChatAPIollama_02_pregunta_usuario.py: escribir una pregunta.
3. ChatAPIollama_03_chat_continuo.py: conversar y conservar el historial.
4. ChatAPIollama_04_chat_streaming.py: mostrar respuestas en tiempo real.
5. Este archivo: conservar la conversación aunque se cierre el programa.
6. Siguiente paso: controlar errores sin cerrar inesperadamente el chat.
"""

# Importa json para leer y escribir el historial de la conversación.
import json

# Importa Path para construir la ruta del archivo de forma segura.
from pathlib import Path

# Importa la librería que permite comunicarse con Ollama desde Python.
import ollama  # pyright: ignore[reportMissingImports]


# Coloca el JSON en la misma carpeta donde se encuentra este programa.
ARCHIVO_HISTORIAL = Path(__file__).with_name("historial_conversacion.json")

# Define el primer mensaje que se usará cuando no exista un historial.
MENSAJE_SISTEMA = {
    "role": "system",
    "content": "Eres un asistente amable y respondes de forma clara."
}

# Comprueba si ya existe una conversación guardada.
if ARCHIVO_HISTORIAL.exists():
    try:
        # Abre el archivo JSON en modo lectura.
        with ARCHIVO_HISTORIAL.open("r", encoding="utf-8") as archivo:
            # Convierte el contenido del JSON nuevamente en una lista de Python.
            mensajes = json.load(archivo)

        # Comprueba que el contenido cargado sea una lista de mensajes.
        if not isinstance(mensajes, list):
            raise ValueError("El historial no contiene una lista.")

        print(f"Se cargaron {len(mensajes)} mensajes del historial.")

    # Si el JSON está dañado, comienza una conversación nueva.
    except (json.JSONDecodeError, OSError, ValueError):
        print("No fue posible leer el historial. Se iniciará uno nuevo.")
        mensajes = [MENSAJE_SISTEMA]
else:
    # Si todavía no existe el JSON, inicia una conversación nueva.
    mensajes = [MENSAJE_SISTEMA]

# Muestra las instrucciones iniciales.
print("Chat con Ollama (historial guardado en JSON)")
print("Escribe 'salir' para terminar.")

# Mantiene el chat activo hasta que el usuario escriba "salir".
while True:
    # Solicita un mensaje al usuario.
    pregunta = input("\nTú: ").strip()

    # Termina el ciclo cuando el usuario escribe "salir".
    if pregunta.lower() == "salir":
        print("Chat: Hasta luego.")
        break

    # Ignora los mensajes vacíos.
    if not pregunta:
        continue

    # Agrega la pregunta al historial que se enviará al modelo.
    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    # Solicita la respuesta por fragmentos para mostrarla en tiempo real.
    respuesta_stream = ollama.chat(
        model="llama3.2:latest",
        messages=mensajes,
        options={
            "temperature": 0.3
        },
        stream=True
    )

    # Aquí se unirán todos los fragmentos de la respuesta.
    texto_respuesta = ""

    print("\nChat: ", end="", flush=True)

    # Recorre e imprime los fragmentos conforme los genera Ollama.
    for fragmento in respuesta_stream:
        texto_fragmento = fragmento["message"]["content"]
        print(texto_fragmento, end="", flush=True)
        texto_respuesta += texto_fragmento

    print()

    # Agrega la respuesta completa al historial de Python.
    mensajes.append(
        {
            "role": "assistant",
            "content": texto_respuesta
        }
    )

    # Abre el JSON en modo escritura; si no existe, Python lo crea.
    with ARCHIVO_HISTORIAL.open("w", encoding="utf-8") as archivo:
        # Guarda la lista con formato legible y conserva los acentos.
        json.dump(mensajes, archivo, ensure_ascii=False, indent=4)

    print(f"Historial guardado en: {ARCHIVO_HISTORIAL.name}")
