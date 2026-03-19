import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. KONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Feinsinn & Flora", 
    page_icon="🌿",
    layout="wide"
)

# --- 2. CSS FÜR PREMIUM LOOK & 'GREAT VIBES' ---
st.markdown("""
<style>
    /* Schriften von Google laden */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Lora:wght@400;700&display=swap');

    /* Hintergrund & Grundschrift */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
        color: #fdf6e3;
        font-family: 'Lora', serif;
    }

    /* Streamlit-Elemente anpassen */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    /* Titel-Styling mit Great Vibes */
    .feinsinn-title {
        font-family: 'Great Vibes', cursive;
        color: #c19a6b;
        font-size: 5.5rem;
        text-align: center;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    
    .feinsinn-subtitle {
        color: #fdf6e3;
        font-family: 'Lora', serif;
        text-align: center;
        margin-top: -15px;
        font-size: 1.1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Karten-Design für die Ergebnisse */
    .result-card {
        background-color: #262626;
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #c19a6b;
        margin-top: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }

    /* Button-Styling */
    .stButton>button {
        background-color: #c19a6b !important;
        color: #1a1a1a !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 15px !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #fdf6e3 !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Schlüssel-Fehler: Bitte prüfe deine Secrets in Streamlit.")
    st.stop()

# Das Modell, das bei deinem Test am besten funktioniert hat
MODEL_NAME = 'gemini-2.5-flash' 

# --- 4. BENUSEROBERFLÄCHE (UI) ---
st.markdown("<h1 class='feinsinn-title'>Feinsinn & Flora</h1>", unsafe_allow_html=True)
st.markdown("<p class='feinsinn-subtitle'>Regionale Garten-Expertise & Lichtdesign</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Layout: Upload und PLZ nebeneinander
col_a, col_b = st.columns([3, 1])

with col_a:
    uploaded_file = st.file_uploader("Dein Gartenfoto", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

with col_b:
    plz = st.text_input("📍 PLZ (für Boden & Klima)", placeholder="z.B. 80331", max_chars=5)

if uploaded_file:
    # Vorschaubild
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True, caption="Ist-Zustand deines Gartens")
    
    # Zentrierter Analyse-Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('✨ EXKLUSIVE ANALYSE STARTEN'):
            with st.spinner('KI-Designer prüft Standortdaten und Ästhetik...'):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    
                    # Der Experten-Prompt mit PLZ-Logik
                    prompt = f"""
                    Du bist Chef-Designer der Premium-Marke 'Feinsinn'. 
                    Der Nutzer befindet sich im Postleitzahlenbereich {plz if plz else 'unbekannt'}.
                    
                    1. Analysiere das Foto.
                    2. Gib 3 exklusive Tipps zu Licht & Holz, die den Garten luxuriöser machen.
                    3. Berücksichtige die PLZ für regionale Besonderheiten (Boden/Klima), falls angegeben.
                    4. Erstelle am Ende einen Abschnitt 'VISUAL PROMPT:'. Beschreibe darin auf Englisch 
                       sehr detailliert eine nächtliche Vision für eine Bild-KI.
                    """
                    
                    response = model.generate_content([prompt, image])
                    
                    # Ergebnis-Anzeige
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown("### 🌿 Dein Feinsinn-Konzept")
                    
                    output = response.text
                    if "VISUAL PROMPT" in output:
                        parts = output.split("VISUAL PROMPT")
                        st.write(parts[0].strip())
                        st.markdown("---")
                        st.markdown("**🎨 Visueller Bauplan für die Nacht:**")
                        st.code(parts[1].replace(":", "").strip(), language="text")
                    else:
                        st.write(output)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Fehler bei der Analyse: {e}")
