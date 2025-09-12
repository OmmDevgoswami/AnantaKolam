import streamlit as st
import requests
import os
import dotenv
dotenv.load_dotenv()

# Sheetly API Config
SHEETLY_API_URL = "https://api.sheety.co/690912ab2d5431ff9ad361fb8b81f47a/sessioRecord/sheet1"
SHEETLY_API_KEY = os.getenv("SHEETLY_API_KEY")  

mentor_data = {
    "JEE": {
        "Mathematics": {"mentor": "Dharmeshwar Mehta", "times": ["10:00 AM", "11:00 AM", "2:00 PM"]},
        "Physics": {"mentor": "Shalini Kapur", "times": ["11:00 AM", "1:00 PM", "3:00 PM"]},
        "Chemistry": {"mentor": "Kritivya", "times": ["12:00 PM", "2:30 PM", "4:00 PM"]},
    },
    "NEET": {
        "Biology": {"mentor": "Ananya Talwar", "times": ["10:30 AM", "12:30 PM", "3:30 PM"]},
        "Physics": {"mentor": "Vishwajeet Patil", "times": ["11:30 AM", "1:30 PM", "4:30 PM"]},
        "Chemistry": {"mentor": "Rishabh Dhanraj", "times": ["12:30 PM", "2:00 PM", "5:00 PM"]},
    },
    "UPSC": {
        "General Knowledge": {"mentor": "Sunil Rao", "times": ["09:00 AM", "11:00 AM", "1:00 PM"]},
        "History": {"mentor": "Vedant Rane", "times": ["10:00 AM", "12:00 PM", "2:00 PM"]},
        "Politics": {"mentor": "Shivanik Sharma", "times": ["11:00 AM", "1:00 PM", "3:00 PM"]},
    }
}

mentor_images = {
    "Dharmeshwar Mehta": "https://ik.imagekit.io/o0nppkxow/Faces/per1.jpeg",
    "Shalini Kapur": "https://ik.imagekit.io/o0nppkxow/Faces/per2.jpeg",
    "Kritivya": "https://ik.imagekit.io/o0nppkxow/Faces/per3.jpeg",
    "Ananya Talwar": "https://ik.imagekit.io/o0nppkxow/Faces/per8.jpeg",
    "Vishwajeet Patil": "https://ik.imagekit.io/o0nppkxow/Faces/per6.jpeg",
    "Rishabh Dhanraj": "https://ik.imagekit.io/o0nppkxow/Faces/per5.jpeg",
    "Sunil Rao": "https://ik.imagekit.io/o0nppkxow/Faces/per10.jpeg",
    "Vedant Rane": "https://ik.imagekit.io/o0nppkxow/Faces/per9.jpeg",
    "Shivanik Sharma": "https://ik.imagekit.io/o0nppkxow/Faces/per7.jpeg",
}

# Function to create mentor slot card
def mentor_slot(subject, mentor_name, time_slots):
    with st.expander(f"📘 {subject} — Meet {mentor_name}"):
        st.image(mentor_images.get(mentor_name, ""), width=150)
        st.markdown(f"**Subject:** {subject}")
        st.markdown(f"**Mentor:** {mentor_name}")

        selected_time = st.selectbox("Pick a Time Slot", time_slots, key=f"time_{subject}")

        name = st.text_input("Your Name", key=f"name_{subject}")
        email = st.text_input("Your Email", key=f"email_{subject}")

        if st.button("Confirm Booking", key=f"btn_{subject}"):
            if name and email:
                booking_data = {
                    "Mentor": mentor_name,
                    "Subject": subject,
                    "Time Slot": selected_time,
                    "User Name": name,
                    "User Email": email
                }
                headers = {
                    "Authorization": f"{SHEETLY_API_KEY}", 
                    "Content-Type": "application/json"
                }
                response = requests.post(SHEETLY_API_URL, json={"sheet1": booking_data}, headers=headers)
                if response.status_code == 200:
                    st.success("Booking Confirmed and Saved!")
                else:
                    st.error("Failed to save booking. Please check your Sheet and tab name.")
            else:
                st.warning("Please enter both Name and Email.")



# Main UI
st.markdown("""
<div style='text-align: center;'>
    <h1>SikshaSathi - ଶିକ୍ଷାସାଥୀ</h1>
    <h2>GuruTalks</h2>
    <h3>From Questions to Confidence — Your Personal Mentor Awaits!</h3>
</div>
""", unsafe_allow_html=True)

exam_choice = st.selectbox("Choose your target exam:", ("JEE", "NEET", "UPSC"), index=None, placeholder="Entrance Preparation...")

if exam_choice:
    subjects = list(mentor_data[exam_choice].keys())
    for subject in subjects:
        mentor_info = mentor_data[exam_choice][subject]
        mentor_slot(subject, mentor_info["mentor"], mentor_info["times"])
