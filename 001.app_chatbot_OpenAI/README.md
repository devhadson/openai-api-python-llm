Este código implementa un **Chatbot personalizado** utilizando la API de OpenAI (GPT-4). Su función principal es actuar como un asistente de ventas o atención al cliente para un negocio textil, ya que carga un catálogo de productos y reglas de negocio específicas antes de iniciar la conversación.

------------------------------------------------------------------------

# Documentación del Chatbot con OpenAI API

Este script de Python permite la interacción con el modelo **GPT-4** de
OpenAI, integrando un contexto específico basado en archivos locales de
productos y reglas de comportamiento.

## Requisitos Previos

-   **Entorno:** Anaconda o entorno virtual de Python.
-   **Librerías:** `openai` (v1.0+).
-   **Archivos Locales:**
    -   `clave_api.txt`: Archivo con la API Key de OpenAI.
    -   `productos_textil.csv`: Catálogo de productos.
    -   `reglas.txt`: Directrices de comportamiento para el bot.

## Análisis del Código por Secciones

### 1. Configuración e Importación de Datos

El script comienza cargando la configuración necesaria desde archivos externos para mantener la seguridad y modularidad.

``` python
import os
import openai
import sys

# Carga de la API Key desde un archivo de texto
with open("clave_api.txt") as archivo:
    openai.api_key = archivo.readline().strip()

# Carga del catálogo de productos
with open("productos_textil.csv") as archivo:
    producto_csv = archivo.read()

# Carga de las reglas de negocio
with open("reglas.txt") as archivo:
    reglas = archivo.read()
```

### 2. Inicialización del Contexto (Memoria del Sistema)

Se utiliza una lista llamada `contexto` para manejar el historial de la
conversación. Se define el rol `system` para establecer la identidad del
bot y cargar la base de conocimientos (productos y reglas).

``` python
contexto = []
# Se inyectan las reglas y el CSV en el mensaje de sistema
contexto.append({'role': 'system', 'content': f"""{reglas} {producto_csv}"""})
```

### 3. Función `enviar_mensajes`

Esta función actúa como la interfaz directa con la API de OpenAI.

-   **Parámetros:** \* `messages`: El historial acumulado.
-   `model`: Por defecto `gpt-4`.
-   `temperature`: Ajustada a `0` para obtener respuestas precisas y
    deterministas.

``` python
def enviar_mensajes(messages, model="gpt-4", temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
```

### 4. Gestión del Flujo de Conversación (`recargar_mensajes`)

Esta función gestiona el ciclo de vida de cada interacción:

1.  Recibe el mensaje del usuario y lo añade al `contexto`.
2.  Llama a la función de envío con una temperatura de `0.7`
    (permitiendo un poco más de creatividad en la charla).
3.  Almacena la respuesta del asistente en el `contexto` para mantener la coherencia en futuros mensajes.

``` python
def recargar_mensajes(charla):
    contexto.append({'role': 'user', 'content': f"{charla}"})
    response = enviar_mensajes(contexto, temperature=0.7)
    contexto.append({'role': 'assistant', 'content': f"{response}"})
    print(f"\n{response}")
```

### 5. Ciclo Principal (`main`)

Implementa un bucle infinito para permitir una conversación continua por consola hasta que el usuario decida salir.

``` python
def main():
    while True:
        mensaje = input("Por favor, ingresa un mensaje (o 'exit' para salir): ")

        if mensaje.lower() == 'exit':
            break

        recargar_mensajes(mensaje)
```

## Flujo de Trabajo

1.  **Inicio:** El script lee los archivos de texto y CSV.
2.  **Configuración:** Se crea un \"System Prompt\" que combina las
    reglas y los productos.
3.  **Iteración:**

-   El usuario escribe una consulta (ej: \"¿Tienen camisas blancas?\").
-   El bot consulta el `contexto` (donde están los productos).
-   La API responde basándose en esos datos.
-   La respuesta se guarda para que el bot \"recuerde\" lo dicho
    anteriormente.

1.  **Cierre:** El proceso termina al escribir `exit`.