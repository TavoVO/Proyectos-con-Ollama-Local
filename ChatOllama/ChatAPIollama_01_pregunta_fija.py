"""
PASO 1: Enviar a Ollama una pregunta fija escrita en el código.
"""

# Importa la librería que permite comunicarse con Ollama desde Python.
import ollama  # pyright: ignore[reportMissingImports]

# Envía los mensajes al modelo y guarda el resultado en "respuesta".
respuesta = ollama.chat(
    # Indica el modelo de Ollama que se utilizará.
    model="llama3.2:latest",

    # Contiene los mensajes que forman la conversación.
    messages=[
        {
            # "system" define el comportamiento que debe seguir el modelo.
            "role": "system",
            "content": "Eres un experto en SQL y respondes claramente."
        },
        {
            # "user" contiene la pregunta o instrucción del usuario.
            "role": "user",
            "content": "Explica: SELECT * FROM usuarios;"
        }
    ],

    # Configura la manera en que el modelo genera su respuesta.
    options={
        # Un valor bajo produce respuestas más predecibles y menos creativas.
        "temperature": 0.2,

        # Limita la cantidad máxima de tokens que puede generar.
        "num_predict": 300
    }
)

# Extrae el texto de la respuesta del modelo y lo muestra en la terminal.
print(respuesta["message"]["content"])
