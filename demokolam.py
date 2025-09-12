import streamlit as st
from PIL import Image
from io import BytesIO
import random
import requests
from requests.utils import quote
import streamlit.components.v1 as components


st.set_page_config(
    page_title="🖌️ Kolam Kraziness",
    page_icon="🌸",
    layout="wide"
)


st.markdown("""
<style>
h1 {
    font-family: 'Pacifico', cursive;
    background: linear-gradient(to right, purple, pink);
    -webkit-background-clip: text;
    color: transparent;
    text-align: center;
    font-size: 60px;
}
.card {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1>🖌️ Kolam Kraziness</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray; font-size:18px;'>Click generate and watch your Kolam dots dance! 🌸✨</p>", unsafe_allow_html=True)


state_prompts = {
    "Tamil Nadu": "A traditional Tamil Nadu Kolam design, symmetric, floral dots",
    "Andhra Pradesh": "A Muggu style border pattern Kolam from Andhra Pradesh, symmetric",
    "Karnataka": "Kolam inspired by Karnataka folk motifs, intricate and symmetric",
    "Kerala": "Kerala floral circular Kolam, vibrant and traditional",
    "Odisha": "Odisha Jhoti Chita style Kolam, intricate and cultural",
    "Maharashtra": "Maharashtra rangoli-inspired Kolam with geometric patterns, colorful",
    "West Bengal": "Alpana style Kolam from West Bengal, intricate floral patterns",
    "Gujarat": "Gujarat traditional rangoli-inspired Kolam, bright and symmetric",
    "Rajasthan": "Rajasthani Kolam with desert motifs, symmetrical and decorative",
    "Punjab": "Punjabi folk art Kolam, floral and vibrant with cultural elements"
}


st.sidebar.header("🎯 Options")
state = st.sidebar.selectbox("Choose a State", [""] + list(state_prompts.keys()))
festival = st.sidebar.selectbox("Choose Festival/Occasion (Optional)", ["None", "Pongal", "Diwali", "Onam", "Holi", "Navratri"])


if festival != "None":
    festival_colors = {
        "Pongal": "#FFF5E6",
        "Diwali": "#1a1a1a",
        "Onam": "#E6FFE6",
        "Holi": "#FFF0F5",
        "Navratri": "#FFF8E1"
    }
    st.markdown(f"<style>body{{background-color: {festival_colors.get(festival, '#FFFFFF')};}}</style>", unsafe_allow_html=True)


if "gallery" not in st.session_state:
    st.session_state.gallery = []


if st.sidebar.button("Generate Kolam"):
    if not state:
        st.warning("⚠️ Please select a state first.")
    else:
        prompt = state_prompts[state]
        if festival != "None":
            prompt += f" for {festival} festival"

        st.info(f"✨ Generating a unique Kolam for {state}...")

        try:
            
            adjectives = ["vibrant", "intricate", "colorful", "modern", "decorative", "traditional", "elegant"]
            layouts = ["symmetrical", "asymmetrical", "circular", "geometric", "ornamental"]
            style = random.choice(adjectives)
            layout_choice = random.choice(layouts)
            unique_prompt = f"{prompt}, {style}, {layout_choice}, --seed {random.randint(1000,9999)}"
            polli_url = f"https://image.pollinations.ai/prompt/{quote(unique_prompt)}"

            with st.spinner("🎨 Generating Kolam..."):
                response = requests.get(polli_url)

            if "image" in response.headers.get("Content-Type", ""):
                img = Image.open(BytesIO(response.content))
                st.session_state.gallery.append((img, state))

           
                components.html("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
                <script>
                confetti({
                  particleCount: 200,
                  spread: 70,
                  origin: { y: 0.6 }
                });
                </script>
                """, height=200)

            else:
                st.error("❌ Pollinations did not return an image. Try again.")

        except Exception as e:
            st.error(f"❌ Could not generate image: {e}")


if st.session_state.gallery:
    img, state_name = st.session_state.gallery[-1]
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image(img, caption=f"🖌️ Kolam of {state_name}", use_container_width=True)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    st.download_button(
        label="⬇️ Download Kolam",
        data=buffer.getvalue(),
        file_name=f"{state_name}_kolam.png",
        mime="image/png"
    )
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.gallery and len(st.session_state.gallery) > 1:
    st.markdown("### 🖼️ Previous Kolams Generated")
    cols = st.columns(3)
    for idx, (img, state_name) in enumerate(st.session_state.gallery[:-1]):
        with cols[idx % 3]:
            st.image(img, caption=f"{state_name}", use_container_width=True)


