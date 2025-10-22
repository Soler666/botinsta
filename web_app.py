import streamlit as st
import threading
from bot_generator import iniciar_bots

st.title("Generador Profesional de Bots para Redes Sociales")

st.markdown("""
Esta aplicación web permite generar bots para interactuar en Instagram y TikTok.
**Nota:** Usa cuentas temporales y respeta las políticas de las plataformas.
""")

# Selección de red social
red_social = st.selectbox("Red Social:", ["Instagram", "TikTok"])

# Entrada de usuario objetivo
usuario = st.text_input("Usuario Objetivo:", placeholder="Ej: usuario_instagram")

# Entrada de cantidad de bots
cantidad = st.number_input("Cantidad de Bots:", min_value=1, max_value=10, value=1, step=1)

# Botón para iniciar
if st.button("Iniciar Bots"):
    if not usuario:
        st.error("Por favor, ingresa el usuario objetivo.")
    else:
        with st.spinner("Ejecutando bots... Esto puede tomar tiempo."):
            # Ejecutar en un hilo separado para no bloquear la UI
            def run_bots():
                result = iniciar_bots(red_social, usuario, cantidad)
                st.success(result)

            thread = threading.Thread(target=run_bots)
            thread.start()
            thread.join()  # Esperar a que termine para mostrar el resultado
