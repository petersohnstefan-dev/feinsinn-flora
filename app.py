import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Feinsinn & Flora", page_icon="🌿")

# 1. Key laden
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Schlüssel-Fehler: {e}")
    st.stop()

st.title("🌿 Feinsinn & Flora")
st.subheader("Visual Design Studio")

# Modell-Setup (Wir bleiben beim stabilen Text-Output)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Gartenfoto hochladen...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Originalzustand', use_column_width=True)
    
    if st.button('Design & Visualisierung planen ✨'):
        with st.spinner('KI-Designer erstellt die Vision...'):
            # Wir fragen nach Text, was die API erlaubt
            prompt = """
            Analysiere dieses Gartenfoto als High-End Licht-Designer. 
            1. Gib 3 Profi-Tipps für die Beleuchtung und Holz-Elemente.
            2. Erstelle am Ende einen 'VISUAL PROMPT'. Das ist eine extrem detaillierte englische Beschreibung 
               für eine Bild-KI, um dieses exakte Bild in eine magische Nachtszene zu verwandeln. 
               Erwähne den Pfad, den Baum und die Terrasse aus dem Foto.
            """
            
            try:
                response = model.generate_content([prompt, image])
                
                st.success("Analyse bereit!")
                
                # Wir trennen Analyse und Prompt optisch
                output = response.text
                if "VISUAL PROMPT" in output:
                    parts = output.split("VISUAL PROMPT")
                    st.markdown("### 💡 Deine Feinsinn-Analyse")
                    st.write(parts[0])
                    
                    st.markdown("---")
                    st.info("🎨 **Der KI-Bauplan für dein Nacht-Bild:**")
                    st.code(parts[1].strip(), language="text")
                else:
                    st.write(output)
                    
            except Exception as e:
                st.error(f"Fehler: {e}")
