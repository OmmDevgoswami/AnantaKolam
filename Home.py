import streamlit as st
from cards import roadmap_card, doubt_clearing_card, mock_test_card, one_on_one_card

st.set_page_config(page_title="SikshaSathi", layout="wide")
st.markdown("""
<div style='text-align: center;'>    
    <img src="https://ik.imagekit.io/o0nppkxow/Kolam_design_5_long.png?updatedAt=1757679235240" alt="AnantaKolam Banner" width = "500" />
    <h1 style='text-align: center;'> AnantaKolam </h1>
    <h3 style='color: gray;'> Infinite patterns, infinite stories. </h3>
    <br />
    <div style='margin-top: 10px;'>
        <a href='https://github.com/OmmDevgoswami/AnantaKolam' target='_blank' style='text-decoration: none; margin: 0 10px;'>🔗 AnantaKolam GitHub</a>
        <p style='color: gray;' > Built using Python - Streamlit, Nanobanana Image Generation and Sutra-multilingual model </p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0].container(height = 380):
    roadmap_card()
with cols[1].container(height = 380):
    doubt_clearing_card()
with cols[0].container(height = 380):
    mock_test_card()
with cols[1].container(height = 380):
    one_on_one_card()