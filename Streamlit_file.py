import streamlit as st
import os
import pandas as pd
from streamlit_calendar import calendar

# Title
st.set_page_config(page_title="Date Luuk", layout="centered")
st.title("❤️ Date Luuk")

# Photo gallery
st.subheader("Swipe through Luuk's photos")

photo_folder = "Data_files/Luuk_photos"
photos = sorted([f for f in os.listdir(photo_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

if "photo_index" not in st.session_state:
	st.session_state.photo_index = 0

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
	st.image(os.path.join(photo_folder, photos[st.session_state.photo_index]), use_column_width=True)

col_left, col_right = st.columns([1, 1])
with col_left:
	if st.button("⟵ Previous"):
		st.session_state.photo_index = (st.session_state.photo_index - 1) % len(photos)
with col_right:
	if st.button("Next ⟶"):
		st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)

# Calendar
st.subheader("📅 Plan your date with Luuk")
st.markdown("Pick a day and suggest your idea for a date.")

csv_path = "Data_files/Luuk_data.csv"

if os.path.exists(csv_path):
	df = pd.read_csv(csv_path)
else:
	df = pd.DataFrame(columns=["title", "start", "end"])

event_data = df.to_dict("records")
calendar_options = {
	"initialView": "dayGridMonth",
	"selectable": True
}

clicked = calendar(events=event_data, options=calendar_options)

with st.form("date_form"):
	name = st.text_input("Your Name")
	idea = st.text_input("What do you want to do on the date?")
	submit = st.form_submit_button("Book This Date")

	if submit and clicked and "start" in clicked and name:
		new_event = {
			"title": name + " - " + idea,
			"start": clicked["start"],
			"end": clicked["start"]
		}
		df = pd.concat([df, pd.DataFrame([new_event])], ignore_index=True)
		df.to_csv(csv_path, index=False)
		st.success(f"Date booked with Luuk on {clicked['start']}!")

