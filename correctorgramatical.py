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

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # Usamos un modelo que sea bueno siguiendo instrucciones
    payload = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": instruccion}], "max_tokens": len(texto_original) + 200, "temperature": 0.2} # Temperatura baja para correcciones precisas

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
        if response.status_code != 200: return f"Error HTTP {response.status_code}: {response.text}"
        data = response.json()
        if "error" in data: return f"Error de OpenRouter: {data['error'].get('message', 'Sin mensaje')}"
        texto_corregido = data["choices"][0]["message"]["content"]
        return texto_corregido.strip()
    except Exception as e:
        return f"Error interno de la aplicación: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("✍️ Corrector Gramatical Básico con IA")
st.write("Pega el texto que quieres revisar y la IA corregirá los errores gramaticales y ortográficos.")

# Columnas para entrada y salida
col1, col2 = st.columns(2)

with col1:
    st.subheader("Texto Original:")
    texto_input = st.text_area("Introduce el texto aquí:", height=300, key="input_text", label_visibility="collapsed")
    
    # Botón de corrección
    boton_corregir = st.button("Corregir Texto")

with col2:
    st.subheader("Texto Corregido:")
    # Placeholder para el área de resultado
    resultado_placeholder = st.empty()
    resultado_placeholder.text_area("La corrección aparecerá aquí...", height=300, key="output_correction_placeholder", disabled=True, label_visibility="collapsed")

# Lógica del botón adaptada para producción
if boton_corregir:
    if not texto_input:
        st.warning("Por favor, introduce algún texto para corregir.")
    # --- Lectura de la API Key desde st.secrets ---
    elif "OPENROUTER_API_KEY" not in st.secrets:
        st.error("Error: La clave API no está configurada en los 'Secrets' de la aplicación.")
    else:
        api_key = st.secrets["OPENROUTER_API_KEY"] # Leer desde secrets
        with st.spinner("Corrigiendo texto..."):
            texto_resultado = corregir_texto(api_key, texto_input) # Pasar la clave leída
            # Actualizamos el placeholder con el resultado
            resultado_placeholder.text_area("Texto Corregido:", value=texto_resultado, height=300, key="output_correction", disabled=True, label_visibility="collapsed")
            st.success("¡Corrección completada!")

