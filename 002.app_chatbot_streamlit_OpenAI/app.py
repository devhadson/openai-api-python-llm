import os
import openai
import streamlit as st

# --- AGREGA ESTO PARA REPARAR EL ERROR ---
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]
# -----------------------------------------

# Leer claves y archivos
with open("clave_api.txt") as archivo:
    openai.api_key = archivo.readline().strip()

with open("ropa_deportiva.csv") as archivo:
    producto_csv = archivo.read()

with open("reglas.txt") as archivo:
    reglas = archivo.read()

# Inicializar contexto en sesión de Streamlit
if "contexto" not in st.session_state:
    st.session_state.contexto = [
        {'role': 'system', 'content': f"{reglas} {producto_csv}"}
    ]

# Función para enviar mensajes al modelo
def enviar_mensajes(messages, model="gpt-4", temperature=0.7):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

# Aplicación Streamlit
st.title("Demo de Chat - Ropas deportivas Sport ⚽ 🏃‍♂️👕")

st.write("Envíanos una consulta para atenderte:")

mensaje = st.text_input("Escribe tu mensaje aquí:")

if st.button("Enviar"):
    if mensaje:
        st.session_state.contexto.append({'role': 'user', 'content': mensaje})
        respuesta = enviar_mensajes(st.session_state.contexto)
        st.session_state.contexto.append({'role': 'assistant', 'content': respuesta})
        st.success(respuesta)
    else:
        st.warning("Por favor escribe un mensaje antes de enviar.")

# Mostrar historial de conversación
st.subheader("Historial de conversación:")
for chat in st.session_state.contexto[1:]:  # Omitimos el primer system prompt
    if chat['role'] == 'user':
        st.markdown(f"**Usuario:** {chat['content']}")
    elif chat['role'] == 'assistant':
        st.markdown(f"**Asistente:** {chat['content']}")