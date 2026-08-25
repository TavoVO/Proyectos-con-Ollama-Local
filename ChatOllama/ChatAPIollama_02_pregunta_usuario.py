"""
PASO 2: Enviar a Ollama una pregunta escrita desde la terminal.

Roadmap:
1. ChatAPIollama_01_pregunta_fija.py: enviar una pregunta fija.
2. Este archivo: permitir que el usuario escriba la pregunta.
3. Siguiente paso: mantener una conversación hasta escribir "salir".
"""

# Importa la librería que permite comunicarse con Ollama desde Python.
import ollama  # pyright: ignore[reportMissingImports]


# Solicita una pregunta y la guarda como texto en la variable "pregunta".
pregunta = input("Escribe tu pregunta: ")

# Envía la pregunta al modelo y guarda el resultado en "respuesta".
respuesta = ollama.chat(
    # Modelo de Ollama instalado en esta computadora.
    model="llama3.2:latest",

    # Mensajes que forman la conversación.
    messages=[
        {
            # Define el comportamiento general del modelo.
            "role": "system",
            "content": "Eres un experto en SQL y respondes claramente."
        },
        {
            # Envía al modelo la pregunta capturada con input().
            "role": "user",
            "content": pregunta
        }
    ],

    # Configura la manera en que el modelo genera la respuesta.
    options={
        # Un valor bajo produce respuestas más predecibles.
        "temperature": 0.2,

        # Limita la cantidad máxima de tokens generados.
        #"num_predict": 300
    }
)

# Imprime un encabezado para separar la pregunta de la respuesta.
print("\nRespuesta:")

# Extrae y muestra el texto generado por el modelo.
print(respuesta["message"]["content"])
