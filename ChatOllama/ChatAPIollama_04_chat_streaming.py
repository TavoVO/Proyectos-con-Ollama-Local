"""
PASO 4: Mantener un chat y mostrar las respuestas en tiempo real.

Roadmap:
1. ChatAPIollama_01_pregunta_fija.py: enviar una pregunta fija.
2. ChatAPIollama_02_pregunta_usuario.py: escribir una pregunta.
3. ChatAPIollama_03_chat_continuo.py: conversar y conservar el historial.
4. Este archivo: mostrar cada respuesta poco a poco con streaming.
5. Siguiente paso: guardar el historial en un archivo JSON.
"""

# Importa la librería que permite comunicarse con Ollama desde Python.
import ollama  # pyright: ignore[reportMissingImports]


# Crea la lista donde se guardará toda la conversación.
mensajes = [
    {
        # Define el comportamiento general del asistente.
        "role": "system",
        "content": "Eres un asistente amable y respondes de forma clara."
    }
]

# Muestra las instrucciones iniciales.
print("Chat con Ollama (streaming)")
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

    # Agrega la pregunta al historial de la conversación.
    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    # Solicita la respuesta con stream=True para recibirla por fragmentos.
    respuesta_stream = ollama.chat(
        model="llama3.2:latest",
        messages=mensajes,
        options={
            "temperature": 0.3
        },
        stream=True
    )

    # Crea una cadena vacía donde se unirán todos los fragmentos.
    texto_respuesta = ""

    # Imprime el nombre del asistente antes de comenzar la respuesta.
    print("\nChat: ", end="", flush=True)

    # Recorre la respuesta conforme Ollama genera cada fragmento.
    for fragmento in respuesta_stream:
        # Extrae el texto del fragmento actual.
        texto_fragmento = fragmento["message"]["content"]

        # Lo muestra inmediatamente sin agregar un salto de línea.
        print(texto_fragmento, end="", flush=True)

        # Lo agrega a la respuesta completa para conservarlo en el historial.
        texto_respuesta += texto_fragmento

    # Agrega un salto de línea cuando termina la respuesta.
    print()

    # Guarda la respuesta completa para recordarla en el siguiente turno.
    mensajes.append(
        {
            "role": "assistant",
            "content": texto_respuesta
        }
    )
