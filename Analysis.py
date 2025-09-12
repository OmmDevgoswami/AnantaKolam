import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from typing import Optional
import os

# Configure page
st.set_page_config(
    page_title="Kolam Art Analyzer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Your API key (replace with your actual API key)
GEMINI_API_KEY = "AIzaSyBMThlSDjHMjrCsfxu8bjUZ8VBkDkCYKHg"

# Fixed prompt for kolam analysis
KOLAM_PROMPT = """If this is a kolam art then only reply otherwise say that "Are you sure this is a kolam?". 

If this is a kolam then list out the following things in a systematic manner:

1. The specific region of India this kolam belongs to?
2. About the mathematical significance of this design
3. Number of grids this kolam has?
4. History of this type of kolam?
5. Its importance"""

# Custom CSS for dark theme and gradient effects
def apply_custom_css():
    st.markdown("""
    <style>
    /* Dark theme background */
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Main gradient title */
    .gradient-title {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f9ca24);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Subtitle gradient */
    .gradient-subtitle {
        background: linear-gradient(45deg, #ffeaa7, #fab1a0, #fd79a8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.3rem !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500 !important;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(45deg, #74b9ff, #0984e3, #6c5ce7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Upload area styling */
    .uploadedFile {
        border: 3px dashed #4ecdc4 !important;
        border-radius: 20px !important;
        background: rgba(78, 205, 196, 0.1) !important;
        padding: 2rem !important;
        text-align: center !important;
        min-height: 200px !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 3px dashed #4ecdc4 !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(69, 183, 209, 0.1) 100%) !important;
        padding: 3rem 2rem !important;
        min-height: 250px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #45b7d1 !important;
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(69, 183, 209, 0.2) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
        border: none !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.6) !important;
    }
    
    /* Info box styling */
    .stInfo {
        background: linear-gradient(135deg, rgba(116, 185, 255, 0.1) 0%, rgba(108, 92, 231, 0.1) 100%) !important;
        border: 1px solid rgba(116, 185, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #74b9ff !important;
    }
    
    /* Success box styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 184, 148, 0.1) 0%, rgba(85, 239, 196, 0.1) 100%) !important;
        border: 1px solid rgba(0, 184, 148, 0.3) !important;
        border-radius: 15px !important;
        color: #00b894 !important;
    }
    
    /* Warning box styling */
    .stWarning {
        background: linear-gradient(135deg, rgba(253, 121, 168, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%) !important;
        border: 1px solid rgba(253, 121, 168, 0.3) !important;
        border-radius: 15px !important;
        color: #fd79a8 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(78, 205, 196, 0.1) 0%, rgba(69, 183, 209, 0.1) 100%) !important;
        border-radius: 10px !important;
        color: #4ecdc4 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 26, 46, 0.5) !important;
        border-radius: 0 0 10px 10px !important;
        border: 1px solid rgba(78, 205, 196, 0.2) !important;
    }
    
    /* Image display enhancement */
    .stImage {
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(78, 205, 196, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stImage:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 12px 40px rgba(78, 205, 196, 0.5) !important;
    }
    
    /* Markdown text styling */
    .stMarkdown {
        color: #fcfafa !important;
    }
    
    /* History section styling */
    .history-title {
        background: linear-gradient(45deg, #a29bfe, #fd79a8, #fdcb6e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem !important;
        font-weight: 600 !important;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
    
    /* Footer styling with kolam-inspired patterns */
    .footer {
        background: 
            radial-gradient(circle at 25% 25%, rgba(108, 92, 231, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(116, 185, 255, 0.15) 0%, transparent 50%),
            repeating-linear-gradient(
                45deg,
                rgba(108, 92, 231, 0.05) 0px,
                rgba(108, 92, 231, 0.05) 2px,
                transparent 2px,
                transparent 20px
            ),
            linear-gradient(90deg, rgba(108, 92, 231, 0.1) 0%, rgba(116, 185, 255, 0.1) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
        border: 1px solid rgba(108, 92, 231, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    /* Add decorative corners to footer */
    .footer::before {
        content: '';
        position: absolute;
        top: 10px;
        left: 10px;
        width: 30px;
        height: 30px;
        background: 
            conic-gradient(from 45deg, 
                rgba(108, 92, 231, 0.3) 0deg, 
                transparent 90deg, 
                rgba(116, 185, 255, 0.3) 180deg, 
                transparent 270deg
            );
        border-radius: 50%;
    }
    
    .footer::after {
        content: '';
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 30px;
        height: 30px;
        background: 
            conic-gradient(from 225deg, 
                rgba(116, 185, 255, 0.3) 0deg, 
                transparent 90deg, 
                rgba(108, 92, 231, 0.3) 180deg, 
                transparent 270deg
            );
        border-radius: 50%;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def initialize_gemini():
    """Initialize Gemini API with the embedded API key"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model, True
    except Exception as e:
        st.error(f"Error initializing Gemini API: {str(e)}")
        return None, False

def analyze_kolam_image(model, image: Image.Image) -> str:
    """Analyze uploaded image for kolam art using Gemini API"""
    try:
        response = model.generate_content([KOLAM_PROMPT, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Header with gradient text
    st.markdown('<h1 class="gradient-title">🎨 Kolam Art Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtitle">Discover the Mathematical Beauty and Cultural Heritage of Traditional Indian Kolam Art</p>', unsafe_allow_html=True)
    
    # Initialize Gemini model
    model, api_success = initialize_gemini()
    
    if not api_success:
        st.error("Failed to initialize the AI model. Please check the API key configuration.")
        return
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown('<h2 class="section-header">📤 Upload Your Image</h2>', unsafe_allow_html=True)
        
        # Enhanced image upload section
        uploaded_file = st.file_uploader(
            "Drag and drop your kolam image here, or click to browse",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload a high-quality image of what you think might be a kolam art pattern"
        )
        
        # Display uploaded image with enhanced styling
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"📸 {uploaded_file.name}", use_container_width=True)
            
            # Enhanced analyze button
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_button = st.button("🔍 Analyze Kolam Pattern", type="primary", use_container_width=True)
        else:
            st.info("👆 Upload an image to begin your kolam journey")
            analyze_button = False
    
    with col2:
        st.markdown('<h2 class="section-header">📋 Analysis Results</h2>', unsafe_allow_html=True)
        
        if analyze_button and uploaded_file and model:
            with st.spinner("🧠 Analyzing patterns and cultural significance..."):
                image = Image.open(uploaded_file)
                analysis_result = analyze_kolam_image(model, image)
                
                # Display results in a beautiful format
                if "Are you sure this is a kolam?" in analysis_result:
                    st.warning(f"🤔 {analysis_result}")
                    st.info("💡 Try uploading a clearer image of a kolam pattern, or learn more about kolam art below!")
                else:
                    st.success("✅ Authentic Kolam Pattern Detected!")
                    
                    # Enhanced results display
                    st.markdown("### 🎯 **Detailed Analysis**")
                    
                    # Parse and format the results beautifully
                    lines = analysis_result.split('\n')
                    formatted_result = ""
                    
                    for line in lines:
                        if line.strip():
                            if any(keyword in line.lower() for keyword in ['region', 'mathematical', 'grids', 'history', 'importance']):
                                formatted_result += f"**{line.strip()}**\n\n"
                            else:
                                formatted_result += f"{line.strip()}\n\n"
                    
                    st.markdown(formatted_result)
                    
                    # Additional enhancement
                    st.markdown("---")
                    st.info("🌟 **Cultural Insight**: This analysis preserves and shares the rich mathematical and spiritual heritage of Indian kolam traditions!")
        
        elif not uploaded_file and analyze_button:
            st.error("Please upload an image first!")
        
        elif not analyze_button:
            # Enhanced about section
            st.markdown("""
            ### 🌸 **About Kolam Art**
            
            Kolam is a **sacred geometric art form** from South India that combines:
            
            ✨ **Spiritual Significance** - Daily offerings to deities  
            🔢 **Mathematical Precision** - Complex geometric patterns  
            👩‍👩‍👧 **Cultural Heritage** - Passed through generations  
            🎨 **Artistic Beauty** - Intricate designs and symmetry  
            
            ---
            
            ### 🚀 **How to Use**
            1. **Upload** a clear image of a kolam pattern
            2. **Click** the analyze button
            3. **Discover** the region, mathematics, and cultural significance
            4. **Learn** about this beautiful traditional art form
            """)
    
    # Initialize session state for history
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []
    
    # Store analysis in history
    if analyze_button and uploaded_file and model:
        image = Image.open(uploaded_file)
        result = analyze_kolam_image(model, image)
        
        # Add to history
        st.session_state.analysis_history.append({
            "image": image,
            "filename": uploaded_file.name,
            "result": result,
            "is_kolam": "Are you sure this is a kolam?" not in result
        })
    
    # Enhanced Analysis History Section
    if st.session_state.analysis_history:
        st.markdown("---")
        st.markdown('<h2 class="history-title">📚 Your Analysis Journey</h2>', unsafe_allow_html=True)
        
        # Display recent analyses with enhanced styling
        for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
            status_emoji = "✅" if analysis['is_kolam'] else "❓"
            status_text = "Verified Kolam" if analysis['is_kolam'] else "Needs Review"
            
            with st.expander(f"{status_emoji} **{analysis['filename']}** - {status_text}", expanded=False):
                col_hist_img, col_hist_result = st.columns([1, 2])
                
                with col_hist_img:
                    st.image(analysis["image"], width=200)
                
                with col_hist_result:
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%); 
                                padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(78, 205, 196, 0.15);'>
                        <h4 style='color: #4ecdc4; font-size: 1.4rem; margin-bottom: 1rem;'>🔍 Analysis Result</h4>
                        <div style='color: white; font-size: 1.1rem; line-height: 1.6;'>{}</div>
                    </div>
                    """.format(analysis["result"].replace('\n', '<br>')), unsafe_allow_html=True)
        
        # Enhanced clear history button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Analysis History"):
            st.session_state.analysis_history = []
            st.rerun()
    
    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <h3 style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem;">
            Kolam Art Analyzer
        </h3>
        <p style="color: #74b9ff; font-size: 1.1rem; margin-bottom: 0.5rem;">
            <strong>Powered by Google Gemini AI</strong>
        </p>
        <p style="color: #a29bfe; font-size: 0.9rem;">
            🌟 Preserving and Understanding the Mathematical Beauty of Traditional Indian Art 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()