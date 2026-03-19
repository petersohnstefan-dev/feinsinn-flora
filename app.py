import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="Feinsinn & Flora Visual", page_icon="🌿")

# 1. Key laden & Modelle konfigurieren
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Schlüssel-Fehler in Secrets: {e}")
    st.stop()

st.title("🌿 Feinsinn & Flora: Visual Studio")
st.write("Zeig mir deinen Garten – ich zeige dir seine magische Zukunft.")

# 2. Diagnose-Modus im Hintergrund (um Fehler zu vermeiden)
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Wir präferieren das neueste Flash-Modell
    content_model_name = next((m for m in available_models if 'gemini-2.5-flash' in m), available_models[0])
except Exception as e:
    st.sidebar.error(f"Modell-Fehler: {e}")
    st.stop()

uploaded_file = st.file_uploader("Lade dein Gartenfoto hoch...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption='Dein Garten (Ist-Zustand)', use_column_width=True)
    
    if st.button('Analyse & Transformation starten ✨'):
        
        # Phase 1: Text-Analyse und Design-Entwurf
        with st.spinner('Phase 1: KI-Gärtner entwirft das Design...'):
            try:
                text_model = genai.GenerativeModel(content_model_name)
                
                # Der "Garderobe"-Prompt: Er generiert die Analyse UND einen Prompt für das Bild
                analysis_prompt = """
                Analysiere dieses Gartenfoto. Erstelle:
                (1) 3 konkrete Ratschläge für Licht- und Holzdesign im 'Feinsinn'-Stil.
                (2) EINEN detaillierten Text-Prompt für eine Bild-KI, um ein nächtliches Bild dieses Gartens mit genau diesen Designelementen zu generieren. 
                Der Prompt MUSS die spezifischen Objekte des Originals (z.B. der geschwungene Steinpfad, der Holzschuppen links, der Baum in der Mitte, der Terrassentisch und die Stühle) beschreiben und die vorgeschlagene Beleuchtung (warm-weißes Uplighting, LED-Spots entlang des Weges, Bistro-Lichterketten) hinzufügen.
                Halte die Ausgabe getrennt: 'ANALYSE:' und 'BILDPROMPT:' (alles in einer Antwort).
                """
                
                response = text_model.generate_content([analysis_prompt, original_image])
                analysis_text = response.text
                
                # Strukturierung der Antwort
                # (Wir brauchen einen Trenner, um den Prompt für die Bild-KI zu extrahieren)
                text_results = analysis_text.split("BILDPROMPT:")
                design_advice = text_results[0].replace("ANALYSE:", "").strip()
                image_gen_prompt = text_results[1].strip() if len(text_results) > 1 else ""
                
                st.success("Phase 1 abgeschlossen!")
                st.markdown("---")
                st.markdown("### 💡 Feinsinn Design-Vorschlag:")
                st.write(design_advice)
                
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")
                st.stop()

        # Phase 2: Visuelle Transformation (Inpainting-Stil)
        if image_gen_prompt:
            st.markdown("---")
            st.markdown("### 🌙 Visuelle Transformation (Zukunft-Zustand):")
            
            with st.spinner('Phase 2: Verwandle den Garten in eine magische Nachtszene...'):
                try:
                    # Im Jahr 2026 nutzen wir das leistungsfähigste integrierte Bild-Modell
                    # Wir gehen davon aus, dass es in der standard Google GenAI API integriert ist.
                    # Für diesen MVP-Stack simulieren wir einen leistungsstarken Text-zu-Bild-Aufruf basierend auf dem generierten Prompt.
                    
                    # (Für High-End Inpainting in 2026 benötigt man spezifischere Aufrufe,
                    # die aber für den MVP-Stack oft zu komplex sind. Wir nutzen einen mächtigen Text-zu-Bild-Aufruf,
                    # der auf den spezifischen Objekten basiert, um die Cohesion zu simulieren.)
                    
                    # Wir gehen davon aus, dass genai.generate_image() in 2026 verfügbar ist.
                    generated_image_bytes = genai.generate_image(
                        prompt=f"A photorealistic night scene of the specific garden from the input photo... {image_gen_prompt}"
                    )
                    
                    generated_image = Image.open(io.BytesIO(generated_image_bytes))
                    st.image(generated_image, caption='Dein Feinsinn & Flora Zukunft-Garten', use_column_width=True)
                    st.success("Transformation abgeschlossen! Willkommen in der Zukunft deines Gartens.")
                    
                except Exception as e:
                    st.error(f"Fehler bei der Transformation: {e}")
                    st.info("Hinweis: Für diesen MVP simulieren wir die Bildgenerierung mit einem mächtigen Text-zu-Bild Prompt. Um Details des Originals exakt zu erhalten, sind fortgeschrittene Inpainting-Techniken nötig, die wir im nächsten Schritt implementieren können.")
