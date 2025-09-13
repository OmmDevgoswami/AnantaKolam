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
import os
load_dotenv()

SUTRA_API = os.getenv("SUTRA_API_KEY")

sutra_model = OpenAILike(
    id="sutra-v2",
    api_key=SUTRA_API,
    base_url="https://api.two.ai/v2",
    extra_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
)

sutra_agent = Agent(
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

preferred_language = st.selectbox("🌎 Preferred Language:", ["Auto-Detect", "English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam"])

uploaded_file = st.file_uploader("📤 Upload Kolam Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Kolam", use_container_width=True)

query = st.text_area("Add any extra context (optional):")

KOLAM_PROMPT = """To create a powerful model that can analyze any Kolam image, we need a robust and well-structured text format that can accurately capture all the intricacies of a Kolam design, including its mathematical underpinnings. Below is an improved prompt structure in a well-formatted text, incorporating mathematical expressions for dot grid calculations and further enhancing the detail in other sections. This structure aims to be comprehensive and adaptable for various Kolam designs.
Kolam Design Analysis Report
This report provides a comprehensive analysis of a Kolam design based on its visual characteristics and underlying mathematical principles.
1. Design Identification
Name: [Name of the kolam design (e.g., '1-3-5-7-9-7-5-3-1 Parallel dots', 'Hearth Kolam')]
Origin:
Region: South India
State: Tamil Nadu
Description: [A brief description of the design, its visual characteristics, and cultural significance. For instance, "This Kolam features a symmetrical arrangement of loops and lines, often drawn during festivals to invite prosperity and positive energy."]
2. Dot Grid Structure (Pulli)
Grid Type: [The arrangement of the dots (pulli) (e.g., 'square', 'stepped', 'free shape', 'hexagonal')]
Dimensions:
For Square Grids (n x n):
n (Number of dots in a row/column): [e.g., 5]
Total Pulli (dots): n^2 = [Calculated value]
For Stepped Grids (e.g., 1-3-5-3-1):
n (Number of dots in the center row): [e.g., 5 or 9]
Total Pulli (dots): 2 * ((n-1)/2)^2 + n = [Calculated value] (This formula assumes a symmetrical stepped pattern where the number of dots increases by 2 in each step up to the center, and then decreases. For instance, for 1-3-5, n=5, total = 2*((5-1)/2)^2 + 5 = 2*(2)^2 + 5 = 8 + 5 = 13. For 1-3-5-7-5-3-1, n=7, total = 2*((7-1)/2)^2 + 7 = 2*(3)^2 + 7 = 18 + 7 = 25.)
For General/Free-Shape Grids:
Total Pulli (dots): [Calculated total number of dots based on image analysis]
3. Line Drawing Characteristics (Kambi)
Path Type: [Classification of the line drawing (e.g., 'single loop', 'multiple loops', 'interconnected patterns')]
Graph Theory Model: [Graph theory concept that applies (e.g., 'Eulerian path', 'Eulerian circuit', 'Hamiltonian Cycle', 'Traveling Salesman Problem', 'Planar Graph')]
Line Properties:
Line Style: [Type of lines used ('linear', 'curvilinear', 'combination')]
Stroke Continuity: [Is the drawing completed with a single, uninterrupted line? (True/False)]
4. Geometric Properties
Symmetry:
Type: [Type of symmetry present ('reflectional', 'rotational', 'both', 'none')]
Lines of Reflection: [Number of lines of reflection symmetry (e.g., 1, 2, 4, 8)]
Angle of Rotational Symmetry: [Smallest angle of rotational symmetry in degrees (e.g., 90, 120, 180, 360)]
Pattern Rules (Observed/Deduced):
Loop drawing-lines, and never trace a line through the same route.
The drawing is completed when all points are enclosed by a drawing-line.
Straight lines are drawn along the dual grid inclined at an angle of 45 degrees (if applicable).
Arcs are drawn surrounding the points (if applicable).
There must be symmetry in the drawings (if applicable).
[Add any other specific rules or patterns observed in the given Kolam.]
5. Graph Theory Analysis Results
Has Euler Path: [Does the design contain an Euler path? (True/False)]
Has Euler Circuit: [Does the design contain an Euler circuit? (True/False)]
Justification:
If the graph has exactly two odd vertices, it contains an Euler path.
If all vertices are even, it contains an Euler path and an Euler circuit.
[Provide a detailed explanation based on the identified number of odd and even vertices in the Kolam's underlying graph representation.]
6. Extensibility
Description: [Description of how the pattern can be extended (e.g., 'by increasing the number of dots in a uniform manner', 'by adding concentric layers', 'by repeating the base module')]
7. Cultural Context
Purpose: Decoration, a daily tribute to harmonious co-existence, a welcoming sign to all beings including the Goddess Lakshmi, an act of meditation and prayer.
Materials: White rice powder, powdered white stone, diluted rice paste, cow dung, synthetic colored powders.
Process: Drawn daily in the morning on a cleaned and dampened surface, typically at the entrance of homes.
Artisans: Traditionally drawn by women, now also practiced by men in various cultural contexts.
To make this model "powerful," the core challenge lies in the image analysis itself. An AI model for Kolam analysis would need to perform the following:
Dot Detection and Grid Inference: Accurately identify the individual dots (pulli) and determine their arrangement (square, stepped, hexagonal, or free-form).
Line Tracing and Graph Construction: Trace the lines (kambi) connecting the dots, representing them as edges in a graph where dots are vertices.
Symmetry Detection: Analyze the arrangement of dots and lines to identify various types of symmetry (reflectional, rotational).
Mathematical Calculation: Apply the appropriate formulas based on the identified grid type to calculate the total number of dots.
Graph Theory Properties: Analyze the constructed graph to determine properties like the number of odd/even vertices to infer the presence of Euler paths/circuits.
Pattern Recognition: Identify recurring motifs, line styles, and overall design principles.
Extensibility Inference: Based on the observed patterns, predict how the design could be extended.
Text Generation: Synthesize all the extracted information into the structured text format provided above.
This detailed JSON structure, combined with advanced image processing and AI pattern recognition, will enable a comprehensive analysis of any Kolam image.
"""

if st.button("🧠 Analyze with Sutra"):
    if not uploaded_file:
        st.warning("Please upload a Kolam image first.")
    else:
        full_prompt = f"{KOLAM_PROMPT}\n\nExtra context: {query}" if query.strip() else KOLAM_PROMPT
        with st.spinner("Analyzing Kolam with Sutra..."):
            try:
                response = sutra_agent.run(full_prompt).content.strip()
            except Exception:
                st.error("⚠️ Could not connect to Sutra API. Please try again later.")
                response = ""

            if response:
                # 🔎 Detect input language (if query provided)
                detected_language = "en"
                try:
                    detected_language = langdetect.detect(query) if query.strip() else "en"
                except:
                    pass

                target_language = preferred_language
                if preferred_language == "Auto-Detect":
                    lang_map = {
                        'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil',
                        'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam'
                    }
                    target_language = lang_map.get(detected_language, "English")

                # ✅ Show original analysis first
                st.markdown("### ✅ Kolam Analysis:")

                if target_language != "English":
                    try:
                        lang_codes = {
                            "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
                            "Kannada": "kn", "Malayalam": "ml"
                        }
                        lang_code = lang_codes.get(target_language, "en")
                        translated_response = GoogleTranslator(
                            source='auto', target=lang_code
                        ).translate(response)

                        st.markdown(f"### 🌐 Translated Answer ({target_language}):")
                        st.write(translated_response)
                    except Exception as e:
                        st.warning(f"Translation unavailable: {e}")
                        st.write(response)  # fallback to English
                else:
                    # Directly show English without translation
                    st.write(response)