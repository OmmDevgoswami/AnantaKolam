import streamlit as st
from google import genai
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
from skimage import feature, filters
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components

# -----------------------------
# CONFIG & API
# -----------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="🎨 AI Kolam Studio", page_icon="🌸", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎨 AI Kolam Generator </h1>", unsafe_allow_html=True)

# -----------------------------
# KOLAM ACCURACY ANALYZER CLASS
# -----------------------------
class KolamAnalyzer:
    def __init__(self):
        self.weights = {
            'symmetry': 0.45,
            'continuous_lines': 0.35,
            'dot_presence': 0.20
        }

    def preprocess_image(self, image):
        """Convert to grayscale + binary for analysis"""
        if isinstance(image, Image.Image):
            img_array = np.array(image.convert('L'))
        else:
            img_array = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = filters.gaussian(img_array, sigma=1.0)
        binary = blurred < filters.threshold_otsu(blurred)
        return (binary.astype(np.uint8) * 255)

    def check_symmetry(self, image):
        processed = self.preprocess_image(image)
        h, w = processed.shape
        left_half = processed[:, :w//2]
        right_half = np.fliplr(processed[:, w//2:])
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        vertical_score = ssim(left_half, right_half)

        top_half = processed[:h//2, :]
        bottom_half = np.flipud(processed[h//2:, :])
        min_height = min(top_half.shape[0], bottom_half.shape[0])
        top_half = top_half[:min_height, :]
        bottom_half = bottom_half[:min_height, :]
        horizontal_score = ssim(top_half, bottom_half)

        return (vertical_score + horizontal_score) / 2

    def check_continuous_lines(self, image):
        processed = self.preprocess_image(image)
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return 0.0
        total_length = sum(cv2.arcLength(c, True) for c in contours)
        avg_length = total_length / len(contours)
        diag = np.sqrt(processed.shape[0] ** 2 + processed.shape[1] ** 2)
        return min(1.0, max(avg_length / (diag * 0.6), 0.0))

    def detect_dots(self, image):
        processed = self.preprocess_image(image)
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 5
        params.maxArea = 200
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(processed)
        return len(keypoints)

    def calculate_overall_accuracy(self, image):
        scores = {}
        scores['symmetry'] = self.check_symmetry(image)
        scores['continuous_lines'] = self.check_continuous_lines(image)
        dot_count = self.detect_dots(image)
        scores['dot_presence'] = min(dot_count / 20, 1.0)
        overall_score = sum(scores[k] * self.weights[k] for k in scores)
        return max(0.0, min(overall_score, 1.0)), scores

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = KolamAnalyzer()
if "gallery" not in st.session_state:
    st.session_state.gallery = []

# -----------------------------
# PROMPT CREATOR
# -----------------------------
def create_advanced_kolam_prompt(kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements):
    return f"""
    Generate a high-quality, symmetric Kolam design with:
    - Base grid: 1-3-5-7-9-7-5-3-1 stepped dot grid
    - Style: Traditional {state} Kolam, smooth white continuous lines on dark wet floor
    - Symmetry: Reflectional + rotational symmetry must be preserved
    - Look: Clean, geometric, elegant, no extra objects, no text
    - Grid size: {grid_size}
    - Complexity: {complexity}
    - Color scheme: {color_scheme} (must follow this palette)
    - Occasion: {occasion}
    - Custom elements: {custom_elements if custom_elements else "Lotus, peacock, temple motifs"}
    Output ONLY a clear single design focused on the Kolam pattern.
    """

# -----------------------------
# SIDEBAR CONFIG
# -----------------------------
st.sidebar.header("🎨 Kolam Design Studio")
col1, col2 = st.sidebar.columns(2)
with col1:
    kolam_type = st.selectbox("Kolam Style", ["Sikku Kolam", "Pulli Kolam", "Rangoli", "Geometric Kolam"], index=1)
    state = st.selectbox("Regional Style", ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Telangana"])
with col2:
    complexity = st.selectbox("Complexity", ["Beginner", "Intermediate", "Advanced"], index=1)
    grid_size = st.slider("Pattern Density", 8, 20, 12)

color_scheme = st.sidebar.selectbox("Color Theme", ["Vibrant Festival", "Royal Colors", "Pastel Dream"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Practice", "Diwali", "Pongal", "Wedding"])
custom_elements = st.sidebar.text_area("Custom Elements", placeholder="peacock motifs, temple arches...", height=80)

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.sidebar.button("✨ Generate Kolam", use_container_width=True):
    with st.spinner("🎭 AI is creating your masterpiece..."):
        try:
            prompt = create_advanced_kolam_prompt(
                kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=prompt
            )

            image_parts = [
                part.inline_data.data
                for part in response.candidates[0].content.parts
                if part.inline_data
            ]

            if image_parts:
                image = Image.open(BytesIO(image_parts[0]))

                # Analyze Image
                overall_score, detailed_scores = st.session_state.analyzer.calculate_overall_accuracy(image)
                st.session_state.gallery.append((image, state, overall_score, detailed_scores))

                # Display
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.image(image, use_container_width=True, caption=f"✨ {kolam_type} Kolam from {state}")
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    st.download_button(
                        label="⬇ Download Kolam",
                        data=buffer.getvalue(),
                        file_name=f"{kolam_type}_{state}_{complexity}.png",
                        mime="image/png"
                    )

                with col2:
                    st.subheader("📊 Kolam Accuracy Analysis")
                    accuracy_percentage = overall_score * 100
                    st.markdown(f"### {'🟢' if accuracy_percentage>70 else '🟡'} Overall Score: {accuracy_percentage:.1f}%")
                    st.progress(overall_score)
                    st.write(f"🔄 Symmetry: {detailed_scores['symmetry']*100:.1f}%")
                    st.write(f"➰ Continuous Lines: {detailed_scores['continuous_lines']*100:.1f}%")
                    st.write(f"⚫ Dot Presence: {detailed_scores['dot_presence']*100:.1f}%")

                components.html("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
                <script>
                confetti({ particleCount: 200, spread: 70, origin: { y: 0.6 } });
                </script>
                """, height=200)

            else:
                st.error("⚠️ No image was generated. Try again with different settings.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# -----------------------------
# GALLERY OF PREVIOUS KOLAMS
# -----------------------------
if st.session_state.gallery:
    st.markdown("### 🖼 Previous Kolams")
    cols = st.columns(3)
    for idx, (img, state_name, acc, _) in enumerate(sorted(st.session_state.gallery, key=lambda x: x[2], reverse=True)):
        with cols[idx % 3]:
            st.image(img, caption=f"{state_name} ({acc*100:.1f}%)", use_container_width=True)
