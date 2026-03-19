import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. KONFIGURATION & BRANDING ---
st.set_page_config(page_title="Feinsinn & Flora", page_icon="🌿", layout="wide")

# --- 2. CSS FÜR PREMIUM LOOK & 'GREAT VIBES' ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Lora:wght@400;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
        color: #fdf6e3;
        font-family: 'Lora', serif;
    }

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
        text-align: center;
        margin-top: -15px;
        font-size: 1.1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    .result-card {
        background-color: #262626;
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #c19a6b;
        margin-top: 25px;
    }

    /* Affiliate Link Styling */
    .shop-item {
        background-color: #333;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #c19a6b;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .shop-button {
        background-color: #c19a6b;
        color: #1a1a1a;
        padding: 8px 15px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
    }

    .stButton>button {
        background-color: #c19a6b !important;
        color: #1a1a1a !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API-Key fehlt.")
    st.stop()

MODEL_NAME = 'gemini-2.5-flash' 

# --- 4. UI ---
st.markdown("<h1 class='feinsinn-title'>Feinsinn & Flora</h1>", unsafe_allow_html=True)
st.markdown("<p class='feinsinn-subtitle'>Design-Atelier & Shop-Kurator</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b = st.columns([3, 1])
with col_a:
    uploaded_file = st.file_uploader("Dein Gartenfoto", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
with col_b:
    plz = st.text_input("📍 PLZ", placeholder="z.B. 80331", max_chars=5)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button('✨ ANALYSE & SHOPPING-LISTE ERSTELLEN'):
        with st.spinner('KI erstellt dein persönliches Design-Paket...'):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                
                # Prompt mit expliziter Shopping-Anweisung
                prompt = f"""
                Du bist Chef-Designer von 'Feinsinn'. PLZ: {plz if plz else 'unbekannt'}.
                1. Analysiere das Foto.
                2. Gib 3 exklusive Tipps zu Licht & Holz.
                3. Nenne 3 konkrete Produkttypen (z.B. 'LED Bodenspot warmweiß'), die für diesen Garten ideal wären.
                4. Erstelle am Ende einen 'VISUAL PROMPT'.
                Antworte strukturiert.
                """
                
                response = model.generate_content([prompt, image])
                
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown("### 🌿 Deine Feinsinn-Expertise")
                st.write(response.text)
                st.markdown("</div>", unsafe_allow_html=True)

                # --- AFFILIATE SEKTION ---
                st.markdown("### 🛒 Shop the Look")
                st.info("Passende Produkte für dein Projekt (Empfehlungen):")
                
                # Hier kannst du später deine echten Affiliate-Links einfügen
                # Beispielhaft für Amazon Suche
                items = ["LED Garten-Spots Warmweiß", "Premium Holz-Lasur Lärche", "Bistro Lichterkette Outdoor"]
                
                for item in items:
                    search_url = f"https://www.amazon.de/s?k={item.replace(' ', '+')}&tag=DEINE_ID-21"
                    st.markdown(f"""
                    <div class='shop-item'>
                        <span>{item}</span>
                        <a href='{search_url}' target='_blank' class='shop-button'>Auf Amazon prüfen ↗</a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"Fehler: {e}")
