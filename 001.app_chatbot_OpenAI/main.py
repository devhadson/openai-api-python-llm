# requisitos Interfase Anaconda libreria OPENAI #licencia activa para el API OPENAI

import os
import openai
import sys

with open("clave_api.txt") as archivo:
    openai.api_key = archivo.readline()

with open("ropa_deportiva.csv") as archivo:
    producto_csv = archivo.read()

with open("reglas.txt") as archivo:
    reglas = archivo.read()

# Creamos la memoria temporal
contexto = []
# registramos las reglas y productos
contexto.append({'role': 'system', 'content': f"""{reglas} {producto_csv}"""})


# enviamos mensaje al modelo
def enviar_mensajes(messages, model="gpt-4", temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


# leemos el mensaje + agregamos al contexto | enviamos el contexto | + agregar respuesta al contexto
def recargar_mensajes(charla):
    contexto.append({'role': 'user', 'content': f"{charla}"})
    response = enviar_mensajes(contexto, temperature=0.7)
    contexto.append({'role': 'assistant', 'content': f"{response}"})
    print()
    print(response)


def main():
    while True:
        print()
        mensaje = input("Por favor, ingresa un mensaje (o 'exit' para salir)")

        if mensaje.lower() == 'exit':
            break

        recargar_mensajes(mensaje)


if __name__ == '__main__':
    main()