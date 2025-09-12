### final roadmap

import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os
import dotenv

# --- Load environment variables ---
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

# --- Configure Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
)
flash_config = LLMConfig(custom_model=gemini_flash)
client = Educhain(flash_config)

# --- Streamlit UI ---
st.set_page_config(page_title="SikshaSathi(ଶିକ୍ଷାସାଥୀ)| AI Smart Lesson", layout="wide")
st.markdown("<h1 style='text-align: center;'>SikshaSathi (ଶିକ୍ଷାସାଥୀ)</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: black;'>Smart Lesson Plan</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: blue;'>Empowering learners with dynamic, AI-generated lessons</h4>", unsafe_allow_html=True)

# --- Input ---
#exam = st.selectbox("🎓 Select Exam", ["Class 10", "Class 12", "JEE", "NEET", "UPSC"])
subject = st.text_input("📘 Enter Subject (e.g., Physics)")
topic = st.text_input("📗 Enter Chapter/Topic (e.g., Light)")
lang = st.selectbox("🌍 Select Language", ["English", "Hindi", "Odia"])
generate = st.button("🚀 Generate Lesson Plan")

# --- Helper to display sections ---
def display_lesson_plan(data):
    st.header(f"📖 {data.get('title', 'Untitled Lesson')}")
    
    st.markdown("### 🎯 Learning Objectives")
    for obj in data.get("learning_objectives", []):
        st.markdown(f"- {obj}")

    st.markdown("### ✨ Introduction")
    st.markdown(data.get("lesson_introduction", "No introduction available."))

    st.markdown("### 🧠 Main Topics")
    for main_topic in data.get("main_topics", []):
        with st.expander(f"📌 {main_topic.get('title', '')}"):
            for sub in main_topic.get("subtopics", []):
                st.markdown(f"#### 🔹 {sub.get('title', '')}")

                if sub.get("key_concepts"):
                    st.markdown("**🧾 Key Concepts:**")
                    for kc in sub["key_concepts"]:
                        st.markdown(f"- *{kc.get('type')}:* {kc.get('content')}")

                if sub.get("discussion_questions"):
                    st.markdown("**💬 Discussion Questions:**")
                    for q in sub["discussion_questions"]:
                        st.markdown(f"- {q.get('question')}")

                if sub.get("hands_on_activities"):
                    st.markdown("**🧪 Hands-on Activities:**")
                    for act in sub["hands_on_activities"]:
                        st.markdown(f"- **{act.get('title')}**: {act.get('description')}")

                if sub.get("reflective_questions"):
                    st.markdown("**🪞 Reflective Questions:**")
                    for rq in sub["reflective_questions"]:
                        st.markdown(f"- {rq.get('question')}")

                if sub.get("assessment_ideas"):
                    st.markdown("**📝 Assessment Ideas:**")
                    for ai in sub["assessment_ideas"]:
                        st.markdown(f"- *{ai.get('type')}*: {ai.get('description')}")

    if data.get("learning_adaptations"):
        st.markdown("### 🧩 Learning Adaptations")
        st.markdown(f"{data['learning_adaptations']}")

    if data.get("real_world_applications"):
        st.markdown("### 🌍 Real-World Applications")
        st.markdown(f"{data['real_world_applications']}")

    if data.get("ethical_considerations"):
        st.markdown("### ⚖️ Ethical Considerations")
        st.markdown(f"{data['ethical_considerations']}")

# --- Generate Lesson Plan ---
if generate and subject and topic:
    with st.spinner("Generating lesson plan..."):
        try:
            prompt = f"""Generate a structured lesson plan for the topic "{topic}" under the subject "{subject}".
The output should be in JSON format with fields like:
- title
- learning_objectives (list)
- lesson_introduction
- main_topics: list of {{
    title: str,
    subtopics: list of {{
        title: str,
        key_concepts: list of {{type, content}},
        discussion_questions: list of {{question}},
        hands_on_activities: list of {{title, description}},
        reflective_questions: list of {{question}},
        assessment_ideas: list of {{type, description}}
    }}
}}
- learning_adaptations
- real_world_applications
- ethical_considerations

Use {lang} for explanations."""

            response = client.content_engine.generate_lesson_plan(prompt)
            lesson_data = response.model_dump() if hasattr(response, "model_dump") else response

            display_lesson_plan(lesson_data)

            st.success("✅ Lesson Plan generated successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    if generate:
        st.warning("⚠️ Please fill all inputs.")

# --- Footer ---
st.markdown("---")
