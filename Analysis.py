import os
import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from dotenv import load_dotenv
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import langdetect
from PIL import Image
from deep_translator import GoogleTranslator

load_dotenv()

SUTRA_API_KEY = os.getenv("SUTRA_API_KEY")

sutra_model = OpenAILike(
    id="sutra-v2",
    api_key=SUTRA_API_KEY,
    base_url="https://api.two.ai/v2",
    extra_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
)

referred_languagesutra_agent = Agent(
    name="Kolam Multilingual Analyzer",
    model=sutra_model,
    instructions=[
        "Be culturally sensitive, clear, and detailed.",
        "Explain the Kolam art type, its regional origin, mathematical significance, grid count, history, and importance in a systematic way.",
        "Respond in the user's preferred language. If you cannot connect to Sutra or face any error, return a short friendly error message instead of crashing."
    ],
    show_tool_calls=False,
    markdown=True,
    add_datetime_to_instructions=False
)

st.set_page_config(page_title="🎨 Kolam Multilingual Analyzer", layout="wide")
st.title("🎨 Kolam Art - Multilingual Analyzer")

p = st.selectbox("🌎 Preferred Language:", ["Auto-Detect", "English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam"])

uploaded_file = st.file_uploader("📤 Upload Kolam Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Kolam", use_container_width=True)

query = st.text_area("Add any extra context (optional):")

KOLAM_PROMPT = """If this is a kolam art then only reply otherwise say that \"Are you sure this is a kolam?\".\n\nIf this is a kolam then list out the following things in a systematic manner:\n\n1. The specific region of India this kolam belongs to?\n2. About the mathematical significance of this design\n3. Number of grids this kolam has?\n4. History of this type of kolam?\n5. Its importance"""

if st.button("🧠 Analyze with Sutra"):
    if not uploaded_file:
        st.warning("Please upload a Kolam image first.")
    else:
        full_prompt = f"{KOLAM_PROMPT}\n\nExtra context: {query}" if query.strip() else KOLAM_PROMPT
        with st.spinner("Analyzing Kolam with Sutra..."):
            try:
                response = sutra_agent.run(full_prompt).content.strip()
            except Exception as e:
                st.error("⚠️ Could not connect to Sutra API. Please try again later.")
                response = ""

            if response:
                detected_language = "English"
                try:
                    detected_language = langdetect.detect(query) if query.strip() else "en"
                except:
                    pass

                target_language = preferred_language
                if preferred_language == "Auto-Detect":
                    lang_map = {'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam'}
                    target_language = lang_map.get(detected_language, "English")

                if target_language != "English":
                    try:
                        translator = Translator()
                        lang_codes = {"Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Malayalam": "ml"}
                        lang_code = lang_codes.get(target_language, "en")
                        translated_response = translator.translate(response, dest=lang_code).text
                        st.markdown(f"### 🌐 Translated Answer ({target_language}):")
                        st.write(translated_response)
                    except Exception as e:
                        st.warning(f"Translation unavailable: {e}")

                st.markdown("### ✅ Kolam Analysis:")
                translated_response = GoogleTranslator(source='auto', target=lang_code).translate(response)
                st.markdown(f"### 🌐 Translated Answer ({target_language}):")
                st.write(translated_response)
