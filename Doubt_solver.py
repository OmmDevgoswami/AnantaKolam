import os
import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import langdetect

load_dotenv()

SUTRA_API_KEY = os.getenv("SUTRA_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

sutra_model = OpenAILike(
    id="sutra-v2",
    api_key=SUTRA_API_KEY,
    base_url="https://api.two.ai/v2"
)

sutra_tools = [TavilyTools(api_key=TAVILY_API_KEY)] if TAVILY_API_KEY else []

sutra_agent = Agent(
    name="SikshaSathi Doubt Solver",
    model=sutra_model,
    tools=sutra_tools,
    instructions=[
        "Be clear, simple, and student-friendly.",
        "Answer doubts related to NEET, JEE, UPSC, or Class XII with helpful context.",
        "Where possible, suggest relevant YouTube videos for better understanding using Tavily.",
        "Always keep tone motivational and easy to grasp."
    ],
    show_tool_calls=True,
    markdown=True,
    add_datetime_to_instructions=False
)

st.set_page_config(page_title="📘 SikshaSathi", layout="wide")
st.title("📘 SikshaSathi - Doubt Solver")

exam_type = st.selectbox("Choose Exam:", ["NEET", "JEE", "UPSC", "Class XII"])
preferred_language = st.selectbox("Preferred Language:", ["Auto-Detect", "English", "Hindi", "Odia"])

import tempfile

audio_input = st.audio_input("🎤 Speak your doubt (optional)")
transcribed_text = ""

if audio_input:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(audio_input.getbuffer())
        tmpfile_path = tmpfile.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(tmpfile_path) as source:
        try:
            audio = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio)
            st.success(f"📝 Transcribed: {transcribed_text}")
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Speech Recognition error: {e}")

query = st.text_area("Type your doubt:", value=transcribed_text)

if st.button("🧠 Get Solution"):
    if not query.strip():
        st.warning("Please enter your doubt.")
    else:
        full_query = f"{exam_type} Doubt: {query}"
        
        with st.spinner("Thinking..."):
            response = sutra_agent.run(full_query).content.strip()
            detected_language = "English"
            try:
                detected_language = langdetect.detect(query)
            except:
                pass

            target_language = preferred_language
            if preferred_language == "Auto-Detect":
                lang_map = {'en': 'English', 'hi': 'Hindi', 'or': 'Odia'}
                target_language = lang_map.get(detected_language, "English")
            if target_language != "English":
                try:
                    translator = Translator()
                    lang_codes = {"Hindi": "hi", "Odia": "or"}
                    lang_code = lang_codes.get(target_language, "en")
                    translated_response = translator.translate(response, dest=lang_code).text
                    st.markdown(f"### 🌐 Translated Answer ({target_language}):")
                    st.write(translated_response)
                except Exception as e:
                    st.warning(f"Translation unavailable: {e}")

            st.markdown("### ✅ AI Answer:")
            st.write(response)

            st.success(f"✅ Detected Language: {target_language}")

            st.markdown("### 📺 Suggested Videos:")
            for line in response.splitlines():
                if "youtube.com/watch" in line:
                    st.markdown(f"[Watch here]({line.strip()})")