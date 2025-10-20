import streamlit as st
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Corrector Gramatical AI", page_icon="✍️", layout="wide")

# --- ESTILO CSS (Opcional) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body { font-family: 'Roboto', sans-serif; }
    h1 { text-align: center; color: #2E8B57; } /* Verde Mar */
    .stButton>button { background-color: #2E8B57; color: white; border-radius: 5px; }
    .stTextArea textarea { border: 1px solid #ccc; border-radius: 5px; }
    #output_correction textarea { /* Estilo específico para el resultado */
        font-family: 'Roboto', sans-serif;
        font-size: 1.1em;
        border: 2px solid #2E8B57;
        height: 300px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE LA API ---
def corregir_texto(api_key, texto_original):
    """Llama a la API de OpenRouter para corregir gramática y ortografía."""
    
    # Meta-prompt específico para corrección
    instruccion = f"""
    Eres un asistente de escritura experto. Tu única tarea es revisar el siguiente texto en busca de errores gramaticales y ortográficos y devolver el texto corregido.
    Realiza únicamente las correcciones necesarias para que el texto sea gramaticalmente correcto y esté bien escrito. No cambies el significado ni el estilo general.
    Devuelve ÚNICAMENTE el texto corregido, sin explicaciones, saludos, comentarios sobre los cambios, ni comillas adicionales.

    Texto a corregir:
    "{texto_original}"
    """

    headers = {"Authorization": f"Bearer {api_key}",
