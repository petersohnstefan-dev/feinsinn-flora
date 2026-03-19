import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Feinsinn & Flora Visual Design", 
    page_icon="🌿",
    layout="wide" # Für mehr Platz
)

# --- CSS SPRIZE FÜR PREMIUM LOOK & 'GREAT VIBES' ---
st.markdown("""
<style>
    /* Google Fonts importieren (Great Vibes für Titel, Lora für Lesbarkeit) */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Lora:ital,wght@0,400..700;1,400..700&display=swap');

    /* Haupt-Hintergrund & Layout (Dunkles Charcoal für edlen Kontrast) */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
        color: #fdf6e3; /* Creme-Schrift */
        font-family: 'Lora', serif; /* Standard-Schrift */
    }

    /* Standard Header ausblenden */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    /* --- TITEL-STYLING (Great Vibes) --- */
    h1.feinsinn-title {
        font-family: 'Great Vibes', cursive;
        color: #c19a6b; /* Messing/Gold-Ton */
        font-size: 6rem;
        text-align: center;
        margin-bottom: 0px;
    }
    h2.feinsinn-subtitle {
        color: #fdf6e3;
        font-family: 'Lora', serif;
        font-weight: 300;
        text-align: center;
        margin-top: -10px;
        font-size: 1.5rem;
    }

    /* --- UNTERSCHRIFTEN & ERGEBNISSE --- */
    h3 {
        color: #c19a6b; /* Messing/Gold-Ton */
        font-family: 'Lora', serif;
        font-weight: 600;
        border-bottom: 1px solid #c19a6b;
        padding-bottom: 5px;
    }

    /* --- INPUT CONTAINER --- */
    [data-testid="stFileUploader"] {
        background-color: #262626;
        padding: 20px;
        border-radius: 10px;
    }

    /* --- OUTPUT CONTAINER --- */
    .feinsinn-result-card {
        background-color: #262626;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* --- CODE BLOCK (VISUAL PROMPT) --- */
    .stCodeBlock {
        background-color: #1a1a1a !important;
        color: #c19a6b !important;
        border: 1px solid #c19a6b !important;
    }
</style>
""", unsafe_allow_html=True)

# --- API SCHLÜSSEL & MODELL-SETUP (Robust) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Schlüssel-Fehler in Secrets: {e}")
    st.stop()

# Wir nutzen gemini-1.5-flash, da es multimodale Transformation unterstützt
# FallsNotFound Fehler kommt, ändere auf gemini-1.5-flash-latest
MODEL_NAME = 'gemini-1.5-flash' 

# --- UI ANZEIGE ---
# Speziell gestalteter Header
st.markdown("<h1 class='feinsinn-title'>Feinsinn & Flora</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='feinsinn-subtitle'>Dein Design-Atelier für Licht & Handwerk</h2>", unsafe_allow_html=True)
st.markdown("---")

# Eingabe-Sektion in einer schicken Karte
with st.container():
    st.markdown("### 1. Lade dein Foto hoch")
    uploaded_file = st.file_uploader("Wähle ein Gartenfoto (JPG, PNG)...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    # Foto anzeigen
    image = Image.open(uploaded_file)
    st.image(image, caption='Dein Garten (Ist-Zustand)', use_column_width=True)
    
    # Der Button (Zentral)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        start_button = st.button('✨ Design-Konzept & Vision planen')

    # --- GENERIERUNGSLOGIK ---
    if start_button:
        with st.spinner('Der KI-Designer erstellt deine Vision...'):
            try:
                # Modell initialisieren (Multimodal Flash)
                model = genai.GenerativeModel(MODEL_NAME)
                
                # Der "Garderobe"-Prompt: Er generiert die Analyse UND einen Prompt für das Bild
                prompt = """
                Du bist ein Experte für Lichtdesign und Gartenarchitektur der Marke 'Feinsinn'. 
                Deine Marke verbindet handwerkliche Feinsinnigkeit mit der Natur.
                Analysiere dieses Foto und erstelle:
                (1) 3 Profi-Ratschläge für die Beleuchtung und passende Holz-Elemente.
                (2) Erstelle am Ende einen Abschnitt 'VISUAL SIGNATURE PROMPT:'. Beschreibe darin auf Englisch 
                   sehr detailliert eine nächtliche, luxuriöse Vision dieses Gartens für eine Bild-KI. 
                   Erhalte die spezifischen Objekte und Strukturen des Originals exakt an ihren Positionen.
                """
                
                # Anfrage senden (Multimodal: Text + Bild)
                response = model.generate_content([prompt, image])
                
                # Ergebnis-Anzeige in einer schicken Karte
                st.markdown("<div class='feinsinn-result-card'>", unsafe_allow_html=True)
                st.markdown("### 2. Deine Feinsinn-Analyse & Vision")
                
                # Strukturierung der Antwort
                output = response.text
                if "VISUAL SIGNATURE PROMPT" in output:
                    parts = output.split("VISUAL SIGNATURE PROMPT")
                    st.write(parts[0].strip())
                    
                    st.markdown("---")
                    st.markdown("🎨 **Die visuelle Signatur deiner Vision:**")
                    st.code(parts[1].replace(":", "").strip(), language="text")
                else:
                    st.write(output)
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.success("Transformation abgeschlossen! Willkommen in der Zukunft deines Gartens.")
                
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")
