import streamlit as st
import requests
# -----------------------------
# Artist Data
# -----------------------------
artist_data = {
    "Pull Kolam": {
        "Intermediate": {"Artist": "Dharmeshwar Mehta", "times": ["10:00 AM", "11:00 AM", "2:00 PM"]},
        "Advanced": {"Artist": "Shalini Kapur", "times": ["11:00 AM", "1:00 PM", "3:00 PM"]},
        "Expert": {"Artist": "Kritivya", "times": ["12:00 PM", "2:30 PM", "4:00 PM"]},
    },
    "Rangoli": {
        "Intermediate": {"Artist": "Ananya Talwar", "times": ["10:30 AM", "12:30 PM", "3:30 PM"]},
        "Advanced": {"Artist": "Vishwajeet Patil", "times": ["11:30 AM", "1:30 PM", "4:30 PM"]},
        "Expert": {"Artist": "Rishabh Dhanraj", "times": ["12:30 PM", "2:00 PM", "5:00 PM"]},
    },
    "Floral Kolam": {
        "Intermediate": {"Artist": "Sunil Rao", "times": ["09:00 AM", "11:00 AM", "1:00 PM"]},
        "Advanced": {"Artist": "Vedant Rane", "times": ["10:00 AM", "12:00 PM", "2:00 PM"]},
        "Expert": {"Artist": "Shivanik Sharma", "times": ["11:00 AM", "1:00 PM", "3:00 PM"]},
    }
}

artist_images = {
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

# -----------------------------
# Helper: Mentor slot card (with form)
# -----------------------------
def mentor_slot(kolam, level, artist_name, time_slots):
    """Render an expander with a booking form for a given kolam-level-artist."""
    if not artist_name:
        st.info("Artist details not available.")
        return

    expander_key = f"exp_{kolam}_{level}"
    form_key = f"form_{kolam}_{level}"

    with st.expander(f"📘 {kolam} — {level} — Meet {artist_name}", expanded=False):
        # artist photo (if available)
        img_url = artist_images.get(artist_name)
        if img_url:
            st.image(img_url, width=150)
        st.markdown(f"**Kolam:** {kolam}")
        st.markdown(f"**Level:** {level}")
        st.markdown(f"**Artist:** {artist_name}")

        # Use a form so the "Confirm Booking" only triggers when user submits
        with st.form(key=form_key):
            selected_time = st.selectbox(
                "Pick a Time Slot",
                time_slots if time_slots else ["No slots available"],
                key=f"time_{kolam}_{level}"
            )
            name = st.text_input("Your Name", key=f"name_{kolam}_{level}")
            email = st.text_input("Your Email", key=f"email_{kolam}_{level}")
            submit = st.form_submit_button("Confirm Booking")

            if submit:
                if not name or not email:
                    st.warning("Please enter both Name and Email.")
                    return

                booking_data = {
                    "Artist": artist_name,
                    "Kolam": kolam,
                    "Level": level,
                    "Time Slot": selected_time,
                    "User Name": name,
                    "User Email": email
                }

                # Build headers
                headers = {"Content-Type": "application/json"}
                if SHEETLY_API_KEY:
                    if SHEETLY_API_KEY.lower().startswith("bearer "):
                        headers["Authorization"] = SHEETLY_API_KEY
                    else:
                        headers["Authorization"] = f"Bearer {SHEETLY_API_KEY}"

                try:
                    resp = requests.post(SHEETLY_API_URL, json={"sheet1": booking_data}, headers=headers, timeout=10)
                    # Accept 200 or 201 as success (Sheety usually returns 201)
                    if resp.status_code in (200, 201):
                        st.success("✅ Booking Confirmed and Saved!")
                    else:
                        st.error(f"❌ Failed to save booking. Status code: {resp.status_code}\n\nResponse: {resp.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Network error while saving booking: {e}")

# -----------------------------
# Main UI
# -----------------------------
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>AnantaKolam — Gurupaints</h1>
        <h3>From artist to art — Your Personal Artist Awaits!</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("---")

# kolam selection
kolam_choice = st.selectbox("Choose your Kolam category:", list(artist_data.keys()))

# show available artists/levels
if kolam_choice:
    levels = artist_data.get(kolam_choice, {})
    if not levels:
        st.info("No artist data available for this kolam.")
    else:
        for level_name, artist_info in levels.items():
            artist_name = artist_info.get("Artist")
            time_slots = artist_info.get("times", [])
            mentor_slot(kolam_choice, level_name, artist_name, time_slots)

st.write("---")
st.info("💡 Add your `SHEETLY_API_KEY` to `.env` for local dev, or to `.streamlit/secrets.toml` for deployment.")
