import streamlit as st
from cards import analysis_card, blog_card, one_on_one_card, kolam_canva_card, kolam_generator_card

pages = [
    st.Page(
        "Home.py",
        title="Home",
        icon=":material/home:"
    ),
    st.Page(
        "Blog.py",
        title="Kolam: Heritage & Culture",
        icon=":material/view_timeline:"
    ),
    st.Page(
        "Analysis.py",
        title="Kolam Decoder",
        icon=":material/analytics:"
    ),
    st.Page(
        "Kolam_Generator.py",
        title="Kolam: Generate Cultural Patterns Digitals",
        icon=":material/analytics:"
    ),
    st.Page(
        "kolam_Canva.py",
        title="Kolam:Canva and Brush",
        icon=":material/palette:"
    ),
    st.Page(
        "Special_One_on_One.py",
        title="Special One-on-One",
        icon=":material/person_raised_hand:"
    )
]

page = st.navigation(pages)
page.run()

with st.sidebar.container(height = 380):
    if page.title == "Kolam: Heritage & Culture":
        blog_card()
    elif page.title == "Kolam Decoder":
        analysis_card()
    elif page.title == "Kolam: Generate Cultural Patterns Digitals":
        kolam_generator_card()
    elif page.title == "Kolam:Canva and Brush":
        kolam_canva_card()
    elif page.title == "Special One-on-One":
        one_on_one_card()
    else:
        st.page_link("Home.py", label="Home", icon=":material/home:")
        st.write("Welcome to the AnantaKolam ")
        st.markdown("""
        <div style='text-align: center;'>
                <img src="https://ik.imagekit.io/o0nppkxow/Kolam_design_5_long%20(1).png?updatedAt=1757718152888" alt="AnantaKolam Banner" width = "200" />
                <h3 style='color: gray;'> Infinite patterns, infinite stories. </h3>
                <br />
                <p style='color: gray;' > Built using Python - Streamlit, Pollination AI Image Generation and Sutra-multilingual model </p>
        </div>
        """, unsafe_allow_html=True)

st.caption("Built with passion by Team Ellipsis 🐦‍🔥🌠")