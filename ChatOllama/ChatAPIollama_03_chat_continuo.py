"""
PASO 3: Mantener un chat continuo con Ollama.

Roadmap:
1. ChatAPIollama_01_pregunta_fija.py: enviar una pregunta fija.
2. ChatAPIollama_02_pregunta_usuario.py: escribir una pregunta en la terminal.
3. Este archivo: conversar varias veces y conservar el historial.
4. Siguiente paso: mostrar cada respuesta en tiempo real.
"""

# Importa la librería que permite comunicarse con Ollama desde Python.
import ollama  # pyright: ignore[reportMissingImports]


# Crea la lista donde se guardará toda la conversación.
mensajes = [
    {
        # El mensaje "system" define cómo debe comportarse el asistente.
        "role": "system",
        "content": "Eres un asistente amable y respondes de forma clara."
    }
]

# Muestra las instrucciones iniciales del programa.
print("Chat con Ollama")
print("Escribe 'salir' para terminar.")

# Mantiene el chat activo hasta que el usuario escriba "salir".
while True:
    # Solicita un mensaje y elimina espacios innecesarios al inicio y al final.
    pregunta = input("\nTú: ").strip()

    # Convierte el texto a minúsculas para aceptar "salir", "SALIR", etc.
    if pregunta.lower() == "salir":
        print("Chat: Hasta luego.")
        break

    # Si el usuario no escribió nada, vuelve a solicitar un mensaje.
    if not pregunta:
        continue

    # Agrega la nueva pregunta al historial de la conversación.
    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    # Envía a Ollama el historial completo para que recuerde el contexto.
    respuesta = ollama.chat(
        # Modelo instalado que generará la respuesta.
        model="llama3.2:latest",

        # Historial con los mensajes de system, user y assistant.
        messages=mensajes,

        # Configura la manera en que el modelo genera sus respuestas.
        options={
            "temperature": 0.3,
            #"num_predict": 300
        }
    )

    # Extrae solamente el texto generado por el modelo.
    texto_respuesta = respuesta["message"]["content"]

    # Muestra la respuesta en la terminal.
    print(f"\nChat: {texto_respuesta}")

    # Guarda la respuesta para que Ollama la recuerde en el siguiente turno.
    mensajes.append(
        {
            "role": "assistant",
            "content": texto_respuesta
        }
    )
