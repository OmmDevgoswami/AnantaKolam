import streamlit as st

def analysis_card():
    st.page_link(page = "Analysis.py" , label = "Aanlysis", icon = ":material/analytics:")
    st.markdown('<h2 class="section-header">📋 Analysis Results</h2>', unsafe_allow_html=True)
        
    analyze_button = st.button("🔍 Analyze Kolam Pattern", type="primary", use_container_width=True)
    if analyze_button and uploaded_file and model:
        with st.spinner("🧠 Analyzing patterns and cultural significance..."):
            image = Image.open(uploaded_file)
            analysis_result = analyze_kolam_image(model, image)

            if "Are you sure this is a kolam?" in analysis_result:
                st.warning(f"🤔 {analysis_result}")
                st.info("💡 Try uploading a clearer image of a kolam pattern, or learn more about kolam art below!")
            else:
                st.success("✅ Authentic Kolam Pattern Detected!")
                st.markdown("### 🎯 **Detailed Analysis**")

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
    
def blog_card():
    st.page_link("Blog.py" , label = "blog", icon = ":material/indeterminate_question_box:")
    user_input = st.text_input("How May i assist you ?", placeholder = "Let's work out this doubt together...")
    audio_input = st.audio_input("Here to help you !!")
    if user_input or audio_input:
        with st.spinner("Generating the Response.."):
            st.success("Content Generated !! Click Here to have the full use of this feature.")
            
def kolam_canva_card():
    st.page_link("Kolam_canva.py" , label = "Canva", icon = ":material/palette:")
    st.header("Canvas & Brush Settings")
    canvas_size = 300
    bg_color = st.color_picker("Background Color", "#071029")
    stroke_width = st.slider("Stroke Width", 1, 20, 3)
    drawing_mode = st.selectbox("Brush Shape", ["freedraw", "line", "circle", "rect"])
    mirror_count = st.selectbox("Number of Mirrors", [1, 2, 4, 6, 8], index=0)
    color_options = {
        "Pink": "#FFD6FF",
        "Cyan": "#66FFF0",
        "Orange": "#FF7B2F",
        "Mint": "#2AF598",
        "Blue": "#00C6FF",
        "Yellow": "#FFFA66",
        "Magenta": "#FF66A3"
    }

    st.write("**Brush Color:**")
    stroke_color = st.session_state.get("selected_color", "#FFD6FF")
    color_cols = st.columns(len(color_options))
    for i, (name, hex_color) in enumerate(color_options.items()):
        if color_cols[i].button(name, key=f"color_{name}"):
            stroke_color = hex_color
            st.session_state["selected_color"] = hex_color
    
def one_on_one_card():
    st.page_link("Special_One_on_One.py" , label = "one_one", icon = ":material/person_raised_hand:")
    choice = st.selectbox("Choose your path",
    ("JEE", "NEET", "UPSC"),
    index = None,
    placeholder = "Guru of Subjects..."
)
    
    card_style = """
    <style>
    .mentor-card {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        width: 300px;
        margin: 0 auto;
    }
    .mentor-card img {
        border-radius: 50%;
        margin-bottom: 15px;
    }
    .mentor-card h3 {
        margin: 10px 0 5px 0;
        color: #4B0082;
    }
    .mentor-card h4 {
        margin: 5px 0;
        color: #555;
    }
    .mentor-card p {
        margin: 8px 0;
        color: #999;
    }
    </style>
"""

    st.markdown(card_style, unsafe_allow_html=True)
    
    if choice == "JEE":
        with st.expander("📘 Meet Dharmeshwar Mehta"):
            st.markdown("""
            <div class='mentor-card'>
                <img src='https://ik.imagekit.io/o0nppkxow/Faces/per1.jpeg?updatedAt=1751628636578' alt='mentor face' width='150' />
                <h3>Dharmeshwar Mehta</h3>
                <h4>Subject: Mathematics</h4>
                <h4>Level: Expert — IIT Gold Medalist</h4>
                <p>“Helping you crack concepts, one formula at a time!”</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("2:30 PM" , type = "secondary")
    elif choice == "NEET":
        with st.expander("📘 Meet Shalini Kapur"):
            st.markdown("""
            <div class='mentor-card'>
                <img src='https://ik.imagekit.io/o0nppkxow/Faces/per2.jpeg?updatedAt=1751628636578' alt='mentor face' width='150' />
                <h3>Shalini Kapur</h3>
                <h4>Subject: Zoology</h4>
                <h4>Level : Stanford Lecturer</h4>
                <p>“Zoology made easy!”</p>
            </div>
            """, unsafe_allow_html=True)
            col = st.columns(2)
            with col[0]:
                st.button("6:00 PM" , type = "secondary")
            with col[1]:
                st.button("8:00 PM" , type = "secondary")
    elif choice == "UPSC":
        with st.expander("📘 Meet Sunil Rao"):
            st.markdown("""
            <div class='mentor-card'>
                <img src='https://ik.imagekit.io/o0nppkxow/Faces/per10.jpeg?updatedAt=1751628636578' alt='mentor face' width='150' />
                <h3>Sunil Rao</h3>
                <h4>Subject: English</h4>
                <h4>Level : UPSC Trainer</h4>
                <p>“Use words to make impact!!”</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("7:30 PM" , type = "secondary")

            