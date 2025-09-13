import streamlit as st
from cards import analysis_card, blog_card, one_on_one_card, kolam_canva_card, kolam_generator_card, community_card

st.set_page_config(page_title="AnantaKolam", layout="wide")

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;600;700&family=Dancing+Script:wght@400;700&display=swap');
    
    /* Hide Streamlit default elements */
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Animated background */
    body {
        background: linear-gradient(-45deg, #FFE4E1, #E6E6FA, #E8F5E8, #FFEAA7);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated Kolam patterns */
    .kolam-pattern-1 {
        width: 60px;
        height: 60px;
        position: relative;
        margin: 20px auto;
        animation: rotate 8s linear infinite;
    }
    
    .kolam-pattern-1::before {
        content: '';
        position: absolute;
        width: 4px;
        height: 4px;
        background: #FF69B4;
        border-radius: 50%;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 
            0 15px 0 #FF69B4,
            0 30px 0 #FF69B4,
            0 45px 0 #FF69B4,
            15px 7.5px 0 #FF1493,
            15px 22.5px 0 #FF1493,
            15px 37.5px 0 #FF1493,
            -15px 7.5px 0 #FF1493,
            -15px 22.5px 0 #FF1493,
            -15px 37.5px 0 #FF1493;
    }
    
    .kolam-pattern-2 {
        width: 80px;
        height: 80px;
        position: relative;
        margin: 20px auto;
        animation: pulse 3s ease-in-out infinite;
    }
    
    .kolam-pattern-2::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid #9370DB;
        border-radius: 50%;
        animation: ripple 2s ease-out infinite;
    }
    
    .kolam-pattern-2::after {
        content: '';
        position: absolute;
        width: 60%;
        height: 60%;
        top: 20%;
        left: 20%;
        border: 2px solid #DA70D6;
        border-radius: 50%;
        animation: ripple 2s ease-out infinite 0.5s;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0.8);
            opacity: 1;
        }
        100% {
            transform: scale(1.2);
            opacity: 0;
        }
    }
    
    .kolam-pattern-3 {
        width: 100px;
        height: 100px;
        position: relative;
        margin: 20px auto;
    }
    
    .kolam-pattern-3::before {
        content: '';
        position: absolute;
        width: 6px;
        height: 6px;
        background: #20B2AA;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow:
            0 -25px 0 #20B2AA,
            25px -25px 0 #20B2AA,
            25px 0 0 #20B2AA,
            25px 25px 0 #20B2AA,
            0 25px 0 #20B2AA,
            -25px 25px 0 #20B2AA,
            -25px 0 0 #20B2AA,
            -25px -25px 0 #20B2AA;
        animation: twinkle 2s ease-in-out infinite;
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Hero section with enhanced animations */
    .hero-section {
        background: linear-gradient(135deg, #FFE4E1 0%, #FFEAA7 50%, #E6E6FA 100%);
        padding: 80px 40px;
        text-align: center;
        border-radius: 30px;
        margin-bottom: 40px;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,182,193,0.3) 2px, transparent 2px);
        background-size: 50px 50px;
        animation: backgroundMove 20s linear infinite;
    }
    
    @keyframes backgroundMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 900;
        color: #2C3E50;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
        text-shadow: 3px 3px 6px rgba(255,255,255,0.8);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { text-shadow: 3px 3px 6px rgba(255,255,255,0.8); }
        to { text-shadow: 3px 3px 20px rgba(255,182,193,0.6), 0 0 30px rgba(255,182,193,0.4); }
    }
    
    .hero-subtitle {
        font-family: 'Dancing Script', cursive;
        font-size: 2rem;
        color: #5D6D7E;
        font-weight: 700;
        position: relative;
        z-index: 2;
        animation: subtitleFloat 4s ease-in-out infinite;
    }
    
    @keyframes subtitleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Enhanced section styling */
    .section-container {
        margin: 40px 0;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .section-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .section-container:hover::before {
        left: 100%;
    }
    
    .section-container:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 10px 25px rgba(0,0,0,0.08);
    }
    
    .section-pink { 
        background: linear-gradient(135deg, #FFE4E1, rgba(255,255,255,0.9));
        border: 1px solid rgba(255,182,193,0.3);
    }
    .section-peach { 
        background: linear-gradient(135deg, #FFEAA7, rgba(255,255,255,0.9));
        border: 1px solid rgba(255,215,0,0.3);
    }
    .section-lavender { 
        background: linear-gradient(135deg, #E6E6FA, rgba(255,255,255,0.9));
        border: 1px solid rgba(147,112,219,0.3);
    }
    .section-mint { 
        background: linear-gradient(135deg, #E8F5E8, rgba(255,255,255,0.9));
        border: 1px solid rgba(144,238,144,0.3);
    }
    .section-blue { 
        background: linear-gradient(135deg, #E6F3FF, rgba(255,255,255,0.9));
        border: 1px solid rgba(173,216,230,0.3);
    }
    .section-coral { 
        background: linear-gradient(135deg, #FFB6C1, rgba(255,255,255,0.9));
        border: 1px solid rgba(255,182,193,0.3);
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #FF69B4, #9370DB);
        border-radius: 2px;
    }
    
    .quote-highlight {
        background: rgba(255,255,255,0.95);
        border-left: 6px solid #FF69B4;
        padding: 25px;
        margin: 25px 0;
        border-radius: 0 20px 20px 0;
        font-style: italic;
        font-size: 1.3rem;
        font-weight: 500;
        color: #2C3E50;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .quote-highlight::before {
        content: '"';
        font-size: 4rem;
        color: #FF69B4;
        opacity: 0.3;
        position: absolute;
        top: -10px;
        left: 10px;
        font-family: 'Playfair Display', serif;
    }
    
    .highlight-box {
        background: rgba(255,255,255,0.8);
        padding: 25px;
        border-radius: 20px;
        margin: 25px 0;
        border: 2px solid rgba(255,182,193,0.4);
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(5px);
    }
    
    .parallax-section {
        background: linear-gradient(45deg, #E6E6FA, #E8F5E8, #FFE4E1);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        padding: 100px 30px;
        text-align: center;
        margin: 60px 0;
        border-radius: 30px;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 0 50px rgba(255,255,255,0.3);
    }
    
    .parallax-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255,182,193,0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(147,112,219,0.3) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(144,238,144,0.3) 0%, transparent 50%);
        animation: backgroundMove 15s ease infinite;
    }
    
    .parallax-text {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: #2C3E50;
        font-weight: 700;
        position: relative;
        z-index: 2;
        animation: sparkle 3s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { 
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(255,182,193,0.5));
        }
        50% { 
            transform: scale(1.05);
            filter: drop-shadow(0 0 20px rgba(255,182,193,0.8));
        }
    }
    
    .emoji-large {
        font-size: 4.5rem;
        margin: 25px 0;
        display: inline-block;
        animation: bounce 2s infinite;
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2));
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0) rotate(0deg); }
        10% { transform: translateY(-10px) rotate(5deg); }
        30% { transform: translateY(-15px) rotate(-5deg); }
        40% { transform: translateY(-10px) rotate(3deg); }
        60% { transform: translateY(-5px) rotate(-2deg); }
    }
    
    /* Enhanced interactive elements */
    .interactive-card {
        background: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .interactive-card:hover {
        border-color: #FF69B4;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255,105,180,0.3);
        background: rgba(255,255,255,0.95);
    }
    
    .floating-decoration {
        position: fixed;
        pointer-events: none;
        z-index: 1;
        opacity: 0.6;
    }
    
    .floating-decoration.dot-1 {
        top: 10%;
        left: 5%;
        animation: floatUpDown 6s ease-in-out infinite;
    }
    
    .floating-decoration.dot-2 {
        top: 20%;
        right: 10%;
        animation: floatUpDown 4s ease-in-out infinite reverse;
    }
    
    .floating-decoration.dot-3 {
        bottom: 30%;
        left: 8%;
        animation: floatUpDown 5s ease-in-out infinite;
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 4.5rem; }
        .hero-subtitle { font-size: 2rem; }
        .section-title { font-size: 2.2rem; }
        .section-container { padding: 25px; margin: 25px 0; }
        .parallax-text { font-size: 2rem; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;' class="hero-section"> 
    <div class="kolam-pattern-2"></div>  
    <div class="kolam-pattern-3"></div>
    <img src="https://ik.imagekit.io/o0nppkxow/Kolam_design_5_long%20(1).png?updatedAt=1757718152888" alt="AnantaKolam Banner" width = "500" />
    <h1 style='text-align: center;' class="hero-title"> AnantaKolam </h1>
    <h3 style='color: gray;' class="hero-subtitle"> Infinite patterns, infinite stories. </h3>
    <br />
    <div style='margin-top: 10px;'>
        <a href='https://github.com/OmmDevgoswami/AnantaKolam' target='_blank' style='text-decoration: none; margin: 0 10px;'>🔗 AnantaKolam GitHub</a>
        <p style='color: gray;' > Built using Python - Streamlit, Pollination AI Image Generation and Sutra-multilingual model </p>
    
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="floating-decoration dot-1">
    <div class="kolam-pattern-1"></div>
</div>
<div class="floating-decoration dot-2">
    <div class="kolam-pattern-2"></div>
</div>
<div class="floating-decoration dot-3">
    <div class="kolam-pattern-3"></div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(3)
with cols[0].container(height = 380):
    blog_card()
with cols[1].container(height = 380):
    analysis_card()
with cols[2].container(height = 380):
    kolam_generator_card()
with cols[0].container(height = 380):
    kolam_canva_card()
with cols[1].container(height = 380):
    one_on_one_card()
with cols[2].container(height = 380):    
    community_card()

st.markdown(""" <div class="kolam-pattern-3"></div> """, unsafe_allow_html=True)