import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Feinsinn & Flora", 
    page_icon="🌿",
    layout="wide"
)

# --- CSS FÜR PREMIUM LOOK & 'GREAT VIBES' ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Lora:wght@400;700&display=swap');

    /* Hintergrund & Grundschrift */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
        color: #fdf6e3;
        font-family: 'Lora', serif;
    }

    /* Titel-Styling */
    .feinsinn-title {
        font-family: 'Great Vibes', cursive;
        color: #c19a6b;
        font-size: 5rem;
        text-align: center;
        margin-bottom: 0px;
        line-height: 1.2;
    }
    .feinsinn-subtitle {
        color: #fdf6e3;
        font-family: 'Lora', serif;
        text-align: center;
        margin-top: -10px;
        font-size: 1.2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Karten-Design für Ergebnisse */
    .result-card {
        background-color: #262626;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #c19a6b;
        margin-top: 20px;
    }

    /* Button-Styling */
    .stButton>button {
        background-color: #c19a6b;
        color: #1a1a1a;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- API SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API-Key fehlt in den Secrets: {e}")
    st.stop()

# Nutzt das Modell, das in deinem Test erfolgreich war
MODEL_NAME = 'gemini-2.5-flash' 

# --- UI ---
st.markdown("<h1 class='feinsinn-title'>Feinsinn & Flora</h1>", unsafe_allow_html=True)
st.markdown("<p class='feinsinn-subtitle'>Exklusive Garten-Visionen</p>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("Lade dein Gartenfoto hoch", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button('✨ DESIGN-KONZEPT ERSTELLEN'):
        with st.spinner('KI-Designer analysiert Strukturen...'):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt = """
                Du bist Chef-Designer der Premium-Marke 'Feinsinn'. 
                Analysiere das Bild und gib 3 exklusive Tipps zu Licht & Holz.
                Erstelle am Ende einen 'VISUAL PROMPT' für ein nächtliches Rendering.
                """
                
                response = model.generate_content([prompt, image])
                
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown("### 💡 Deine Feinsinn-Expertise")
                
                output = response.text
                if "VISUAL PROMPT" in output:
                    parts = output.split("VISUAL PROMPT")
                    st.write(parts[0].strip())
                    st.markdown("---")
                    st.markdown("**🎨 Visueller Bauplan für die Nacht:**")
                    st.code(parts[1].strip(), language="text")
                else:
                    st.write(output)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Fehler: {e}")
