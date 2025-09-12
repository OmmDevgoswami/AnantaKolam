import streamlit as st
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="Kolam: Heritage & Culture", page_icon="🎨", layout="wide")

# --- Intro Section ---
st.title("🎨 Kolam: The Living Heritage of India")
st.markdown("""
Kolam is a traditional South-Indian floor-drawing practice using rice flour or colored powders.
It represents a unique blend of art, mathematics, and culture—drawn daily at dawn, renewing life and inviting prosperity.
Let's walk through its evolution across India in a **timeline journey**.
""")

# --- Timeline Section ---
st.header("🕰️ Timeline of Kolam & Regional Variations")

timeline_data = [
    {"year": "Prehistoric / Folk Origins", "event": "Early geometric and dot patterns practiced as part of fertility and prosperity rituals."},
    {"year": "Medieval Era (13th c.)", "event": "Earliest inscriptions referencing Kolam appear in Tamil Nadu temple records."},
    {"year": "Colonial Era (18th-19th c.)", "event": "Ethnographers document Kolam, Muggulu, Alpana, Aipan across India as cultural markers."},
    {"year": "Modern Day", "event": "Kolam evolves into competitions, festivals, digital apps, and algorithmic research in math & computer science."},
]

for item in timeline_data:
    with st.container():
        st.subheader(f"📅 {item['year']}")
        st.write(item['event'])

# --- Regional Distribution ---
st.header("🗺️ Regional Footprint")
st.markdown("""
- **Tamil Nadu / Karnataka / Kerala:** Pulli & Sikku Kolams dominate.
- **Andhra & Telangana:** Muggulu with dots and bright colors.
- **Maharashtra & Gujarat:** Rangoli with freehand floral & geometric patterns.
- **West Bengal:** Alpana using rice paste, circular motifs.
- **Uttarakhand:** Aipan drawn with ochre-red background.
- **Odisha:** Jhoti with finger-drawn white paste motifs.
""")

# --- Images Section ---
st.header("🖼️ Visual Highlights")
col1, col2 = st.columns(2)
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Pulli_kolam.jpg/440px-Pulli_kolam.jpg", caption="Pulli Kolam")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Kolam_sikku.jpg/440px-Kolam_sikku.jpg", caption="Sikku Kolam")
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Rangoli_Design.jpg/440px-Rangoli_Design.jpg", caption="Rangoli Design")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Alpana.jpg/440px-Alpana.jpg", caption="Bengali Alpana")

# --- Closing Note ---
st.markdown("---")
st.markdown("Kolam is a **living heritage** — a daily ritual that combines art, devotion, and science. Preserving and sharing it keeps this cultural rhythm alive for generations ✨")
