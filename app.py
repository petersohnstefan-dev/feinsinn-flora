import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Feinsinn & Flora Debug", page_icon="🌿")

# 1. Key laden
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Schlüssel-Fehler: {e}")
    st.stop()

st.title("🌿 Feinsinn & Flora: Diagnose-Modus")

# 2. Verfügbare Modelle prüfen (Das löst das Rätsel)
st.sidebar.write("### Verfügbare Modelle:")
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.sidebar.json(available_models)
    # Wir nehmen automatisch das erste Flash-Modell, das wir finden
    default_model = next((m for m in available_models if 'flash' in m), available_models[0])
except Exception as e:
    st.sidebar.error(f"Modell-Liste fehlgeschlagen: {e}")
    default_model = "gemini-1.5-flash" # Fallback

uploaded_file = st.file_uploader("Foto hochladen...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    # Modell-Auswahl für dich zum Testen
    selected_model_name = st.selectbox("Wähle ein Modell aus:", available_models, index=available_models.index(default_model) if default_model in available_models else 0)
    
    if st.button('Analyse starten'):
        try:
            model = genai.GenerativeModel(selected_model_name)
            prompt = "Du bist Garten-Designer. Gib 3 kurze Tipps zu Licht und Holz für diesen Garten."
            
            with st.spinner(f'Nutze Modell: {selected_model_name}...'):
                response = model.generate_content([prompt, image])
                st.success("Erfolg!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Fehler bei der Generierung: {e}")
            st.info("Tipp: Wenn 'NotFound' erscheint, versuche ein anderes Modell aus der Liste oben links.")
