import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Feinsinn & Flora", page_icon="🌿")

# Wir holen uns den Key sicher aus den "Secrets" von Streamlit (erkläre ich gleich)
api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("🌿 Feinsinn & Flora")
st.write("Lade dein Foto hoch für eine exklusive Design-Analyse.")

uploaded_file = st.file_uploader("Wähle ein Gartenfoto...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button('Garten-Potenzial analysieren'):
        with st.spinner('KI-Gärtner bei der Arbeit...'):
            prompt = "Analysiere dieses Bild als Garten-Designer. Wo passen Lichtakzente? Welche Holz-Elemente von 'Feinsinn' würden hier harmonieren?"
            response = model.generate_content([prompt, image])
            st.markdown("### ✨ Dein Design-Vorschlag:")
            st.write(response.text)
