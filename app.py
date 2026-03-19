import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Feinsinn & Flora", page_icon="🌿")

# 1. API-Schlüssel sicher laden
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Schlüssel-Fehler: {e}")
    st.stop()

st.title("🌿 Feinsinn & Flora")
st.write("Dein Design-Studio für Licht & Handwerk.")

# Wir nutzen das Modell, das bei dir vorhin funktioniert hat!
MODEL_NAME = 'gemini-2.5-flash' 

uploaded_file = st.file_uploader("Gartenfoto hochladen...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Dein Garten (Original)', use_column_width=True)
    
    if st.button('Design-Konzept erstellen ✨'):
        with st.spinner('KI-Designer erstellt deine Vision...'):
            try:
                # Modell initialisieren
                model = genai.GenerativeModel(MODEL_NAME)
                
                prompt = """
                Analysiere dieses Foto als High-End Garten-Designer der Marke 'Feinsinn'. 
                1. Gib 3 Profi-Tipps für die Beleuchtung und passende Holz-Elemente.
                2. Erstelle am Ende einen Abschnitt 'VISUAL PROMPT'. Beschreibe darin auf Englisch 
                   sehr detailliert eine nächtliche, luxuriöse Version dieses Gartens für eine Bild-KI.
                """
                
                # Anfrage senden
                response = model.generate_content([prompt, image])
                
                # Ergebnis anzeigen
                st.success("Analyse fertig!")
                output = response.text
                
                if "VISUAL PROMPT" in output:
                    parts = output.split("VISUAL PROMPT")
                    st.markdown("### 💡 Deine Feinsinn-Analyse")
                    st.write(parts[0].strip())
                    
                    st.markdown("---")
                    st.info("🎨 **Der Prompt für dein Nacht-Bild:**")
                    st.code(parts[1].replace(":", "").strip(), language="text")
                else:
                    st.write(output)
                    
            except Exception as e:
                st.error(f"Fehler bei der Anfrage: {e}")
                st.info("Falls das Modell nicht gefunden wird, probieren wir gleich eine dynamische Liste.")
