#final
import streamlit as st
import time
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()


GOOGLE_API_KEY = os.getenv("GEMINI_KEY")
# --- Setup Gemini model ---
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key =  GOOGLE_API_KEY
)
gemini_config = LLMConfig(custom_model=gemini_model)
client = Educhain(gemini_config)

# --- Initialize session state ---
if "questions" not in st.session_state:
    st.session_state.questions = None
    st.session_state.submitted = []
    st.session_state.answers = []
    
    # --- Logo ---
# --- Top-left logo using HTML ---


    

# --- Title ---
st.markdown("<h1 style='text-align: center;'>SikshaSathi (ଶିକ୍ଷାସାଥୀ)</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Exam Master</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: blue;'>Practice Smart. Learn Fast. Shine Bright!</h4>", unsafe_allow_html=True)

# --- User Inputs ---
exam = st.selectbox("🎓 Select Exam", ["Class 10", "Class 12", "JEE", "NEET", "UPSC"])

subject_options = {
    "Class 10": ["Science", "Math", "Social Science"],
    "Class 12": ["Physics","Mathematics", "Chemistry", "Biology",],
    "JEE": ["Physics", "Chemistry", "Maths"],
    "NEET": ["Physics", "Chemistry", "Biology"],
    "UPSC": ["History", "Geography", "Polity"]
}
subject = st.selectbox("📘 Select Subject", subject_options[exam])

chapter_options = {
    "Physics": [
    "Units and Measurements",
    "Motion in a Straight Line",
    "Motion in a Plane",
    "Laws of Motion",
    "Work, Energy and Power",
    "System of Particles and Rotational Motion",
    "Gravitation",
    "Mechanical Properties of Solids",
    "Mechanical Properties of Fluids",
    "Thermal Properties of Matter",
    "Thermodynamics",
    "Kinetic Theory of Gases",
    "Oscillations",
    "Waves",
    "Electric Charges and Fields",
    "Electrostatic Potential and Capacitance",
    "Current Electricity",
    "Moving Charges and Magnetism",
    "Magnetism and Matter",
    "Electromagnetic Induction",
    "Alternating Current",
    "Ray Optics and Optical Instruments",
    "Wave Optics",
    "Dual Nature of Radiation and Matter",
    "Atoms",
    "Nuclei",
    "Semiconductor Electronics",
    "Communication Systems"
]
,
"Mathematics": [
    "Relations and Functions",
    "Inverse Trigonometric Functions",
    "Matrices",
    "Determinants",
    "Continuity and Differentiability",
    "Applications of Derivatives",
    "Integrals",
    "Applications of Integrals",
    "Differential Equations",
    "Vector Algebra",
    "Three Dimensional Geometry",
    "Linear Programming",
    "Probability"
],

    "Chemistry": [
    "Some Basic Concepts of Chemistry",
    "Structure of Atom",
    "Classification of Elements and Periodicity in Properties",
    "Chemical Bonding and Molecular Structure",
    "States of Matter: Gases and Liquids",
    "Thermodynamics",
    "Equilibrium",
    "Redox Reactions",
    "Hydrogen",
    "The s-Block Element",
    "Some p-Block Elements",
    "Organic Chemistry - Basic Principles and Techniques",
    "Hydrocarbons",
    "Environmental Chemistry",
    "The Solid State",
    "Solutions",
    "Electrochemistry",
    "Chemical Kinetics",
    "Surface Chemistry",
    "The p-Block Element",
    "The d- and f-Block Elements",
    "Coordination Compounds",
    "Haloalkanes and Haloarenes",
    "Alcohols, Phenols and Ethers",
    "Aldehydes, Ketones and Carboxylic Acids",
    "Organic Compounds Containing Nitrogen",
    "Biomolecules",
    "Polymers",
    "Chemistry in Everyday Life"
]
,
    "Biology": [
    "Diversity of Living Organisms",
    "Structural Organisation in Animals and Plants",
    "Cell Structure and Function",
    "Plant Physiology",
    "Human Physiology",
    "Reproduction",
    "Genetics and Evolution",
    "Biology and Human Welfare",
    "Biotechnology and Its Applications",
    "Ecology and Environment"
]
,
    "Maths": [
    "Sets, Relations and Functions",
    "Complex Numbers and Quadratic Equations",
    "Matrices and Determinants",
    "Permutations and Combinations",
    "Binomial Theorem and Its Applications",
    "Sequences and Series",
    "Limits, Continuity and Differentiability",
    "Integral Calculus",
    "Differential Equations",
    "Coordinate Geometry",
    "Three Dimensional Geometry",
    "Vector Algebra",
    "Statistics and Probability",
    "Trigonometry",
    "Mathematical Reasoning"
],
    

    "History": [
  "Prehistoric Cultures in India",
  "Indus Valley Civilization",
  "Vedic Age and Later Vedic Age",
  "Mahajanapadas and Rise of Magadh",
  "Mauryan Empire",
  "Post-Mauryan Period (Shungas, Kushanas, Satavahanas)",
  "Gupta Empire and Post-Gupta Period",
  "Harsha and his Times",
  "Early Medieval India (750–1200 AD)",
  "Delhi Sultanate",
  "Vijayanagara and Bahmani Kingdoms",
  "Mughal Empire",
  "Maratha Confederacy",
  "Advent of Europeans in India",
  "British Expansion in India",
  "Economic Impact of British Rule",
  "Socio-Religious Reform Movements",
  "Revolt of 1857",
  "Indian National Movement (1885–1947)",
  "Gandhian Era and Mass Movements",
  "Constitutional Developments",
  "Quit India Movement",
  "Indian Independence Act 1947",
  "World War I and its Impact on India",
  "World War II and Freedom Struggle",
  "Integration of Princely States",
  "History of Post-Independence India",
  "World History: French Revolution",
  "World History: American Revolution",
  "World History: Russian Revolution",
  "World History: Industrial Revolution",
  "World History: World War I",
  "World History: World War II",
  "Cold War and its Impact"
]
,
    "Geography": [
  "Geomorphology (Landforms and Processes)",
  "Climatology (Atmosphere and Weather)",
  "Oceanography (Waves, Tides, Currents)",
  "Continents and Oceans",
  "Distribution of Natural Resources",
  "Indian Physiography",
  "Indian Climate",
  "Indian Drainage System",
  "Soils of India",
  "Natural Vegetation of India",
  "Indian Agriculture",
  "Irrigation and Cropping Patterns in India",
  "Minerals and Energy Resources (India and World)",
  "Industries in India",
  "Transport and Communication",
  "Population and Migration",
  "Urbanization and Settlements",
  "World Physical Features (Mountains, Plateaus, Plains)",
  "Geographical Location of India",
  "Time Zones and Standard Time",
  "Disaster Management and Geography",
  "Environmental Geography",
  "Biogeography",
  "Map-Based Questions (India and World)",
  "Remote Sensing and GIS (Basics)",
  "Current Affairs related to Geography (like Cyclones, Earthquakes)"
]
,
    "Polity": [
  "Historical Background of Indian Constitution",
  "Making of the Constitution",
  "Salient Features of the Constitution",
  "Preamble of the Constitution",
  "Union and its Territory",
  "Citizenship",
  "Fundamental Rights",
  "Directive Principles of State Policy",
  "Fundamental Duties",
  "Amendment of the Constitution",
  "Basic Structure Doctrine",
  "Parliamentary System",
  "Federal System",
  "Centre-State Relations",
  "Inter-State Relations",
  "Emergency Provisions",
  "President and Vice-President",
  "Prime Minister and Council of Ministers",
  "Parliament (Lok Sabha and Rajya Sabha)",
  "Judiciary (Supreme Court, High Court, Subordinate Courts)",
  "Governor",
  "Chief Minister and State Council of Ministers",
  "State Legislature",
  "Union Territories and Special Areas",
  "Panchayati Raj",
  "Municipalities",
  "Union Public Service Commission (UPSC)",
  "State Public Service Commissions",
  "Finance Commission",
  "Election Commission",
  "Comptroller and Auditor General (CAG)",
  "Attorney General and Advocate General",
  "Official Language",
  "Special Provisions for SCs, STs, BCs, and Minorities",
  "Tribunals and Quasi-Judicial Bodies",
  "Co-operative Societies",
  "Important Constitutional and Non-Constitutional Bodies",
  "Recent Constitutional Amendments",
  "Landmark Supreme Court Judgments"
]
,
    "Science": [
  "Chemical Reactions and Equations",
  "Acids, Bases and Salts",
  "Metals and Non-metals",
  "Carbon and its Compounds",
  "Periodic Classification of Elements",
  "Life Processes",
  "Control and Coordination",
  "How do Organisms Reproduce?",
  "Heredity and Evolution",
  "Light – Reflection and Refraction",
  "The Human Eye and the Colourful World",
  "Electricity",
  "Magnetic Effects of Electric Current",
  "Sources of Energy",
  "Our Environment",
  "Sustainable Management of Natural Resources"
],
    "Math": [
        "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables",
        "Quadratic Equations", "Arithmetic Progression", "Triangles",
        "Coordinate Geometry", "Introduction to Trigonometry", "Applications of Trigonometry",
        "Circles", "Constructions", "Areas Related to Circles",
        "Surface Areas and Volumes", "Statistics", "Probability"
    ]
,
   "Social Science": [
  "The Rise of Nationalism in Europe",
  "Nationalism in India",
  "The Making of a Global World",
  "The Age of Industrialisation",
  "Print Culture and the Modern World",
  "Resources and Development",
  "Forest and Wildlife Resources",
  "Water Resources",
  "Agriculture",
  "Minerals and Energy Resources",
  "Manufacturing Industries",
  "Lifelines of National Economy",
  "Power Sharing",
  "Federalism",
  "Gender, Religion and Caste",
  "Political Parties",
  "Outcomes of Democracy",
  "Development",
  "Sectors of the Indian Economy",
  "Money and Credit",
  "Globalisation and the Indian Economy",
  "Consumer Rights"
]
,
}
topic_list = chapter_options.get(subject, [])
topic = st.selectbox("📖 Select Chapter/Topic", topic_list)

level = st.selectbox("🎯 Select difficulty level:", ["Easy", "Medium", "Hard"])
question_type = st.selectbox("❓ Select the type of questions:", ["Multiple Choice", "Fill in the Blank"])
num_questions = st.slider("📊 Number of Questions:", 1, 10, 3)

# --- Generate Button ---
if st.button("🎯 Generate Questions"):
    with st.spinner("🔄 Generating Questions..."):
        question = client.qna_engine.generate_questions(
            topic=topic,
            num=num_questions,
            question_type=question_type,
            difficulty_level=level
        )

        data = question.model_dump()
        st.session_state.questions = data["questions"]
        st.session_state.submitted = [False] * len(data["questions"])
        st.session_state.answers = [""] * len(data["questions"])

# --- Show Questions ---
if st.session_state.questions:
    st.header(f"📄 Questions on: {topic}")

    for i, q in enumerate(st.session_state.questions):
        with st.container():
            st.subheader(f"Q{i+1}: {q['question']}")
            st.markdown(f"🧠 Difficulty: **{level}**")

            if question_type == "Multiple Choice":
                user_answer = st.radio("Choose an option:", q["options"], key=f"answer_{i}")
            elif question_type == "Fill in the Blank":
                user_answer = st.text_input("Your answer:", key=f"answer_{i}")

            st.session_state.answers[i] = user_answer

            if st.button(f"✅ Submit Q{i+1}", key=f"submit_{i}"):
                st.session_state.submitted[i] = True

            if st.session_state.submitted[i]:
                if st.session_state.answers[i] == q["answer"]:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. Correct answer: **{q['answer']}**")
                st.markdown(f"**Explanation:** {q['explanation']}")
                st.markdown("---")

# --- Final Scoreboard ---
if st.session_state.questions is not None and all(st.session_state.submitted):
    total = len(st.session_state.questions)
    correct = sum(
        st.session_state.answers[i] == st.session_state.questions[i]["answer"]
        for i in range(total)
    )
    wrong = total - correct
    score_percent = int((correct / total) * 100)

    if score_percent == 100:
        badge = "🏅 Perfect!"
    elif score_percent >= 80:
        badge = "🎉 Excellent!"
    elif score_percent >= 60:
        badge = "👍 Good Job!"
    elif score_percent >= 40:
        badge = "📘 Keep Practicing!"
    else:
        badge = "💡 Don’t give up!"

    st.markdown("## 🧾 **Quiz Summary**")
    st.markdown(f"**✅ Correct:** `{correct}`  \n**❌ Incorrect:** `{wrong}`  \n**📊 Score:** `{score_percent}%`")
    st.write("Your Progress:")
    st.progress(score_percent / 100)
    st.success(f"{badge}")
