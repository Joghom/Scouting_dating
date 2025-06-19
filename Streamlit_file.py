import streamlit as st
import os
import pandas as pd
from streamlit_calendar import calendar

# hide Streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# page setup
st.set_page_config(page_title="Date Luuk", layout="centered")
st.title("Date Luuk")

# photo gallery
st.subheader("Swipe through Luuk's photos")
photo_folder = "Data_files/Luuk_photos"
photos = sorted([f for f in os.listdir(photo_folder) if f.lower().endswith(( '.png', '.jpg', '.jpeg' ))])
if "photo_index" not in st.session_state:
	st.session_state.photo_index = 0
left_col, image_col, right_col = st.columns([1,2,1])
with image_col:
	st.image(
		os.path.join(photo_folder, photos[st.session_state.photo_index]),
		width=400
	)
with left_col:
	if st.button("Previous"):
		st.session_state.photo_index = (st.session_state.photo_index - 1) % len(photos)
with right_col:
	if st.button("Next"):
		st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)

# calendar planning
st.subheader("Plan your date with Luuk")
st.markdown("Pick a day and suggest your idea for a date.")
csv_path = "Data_files/Luuk_data.csv"

# load or create data file
if os.path.exists(csv_path):
	df = pd.read_csv(csv_path)
else:
	df = pd.DataFrame(columns=["Name","date","end","discription"])

# prepare events for calendar
event_records = []
for _, row in df.iterrows():
	title = f"{row['Name']} - {row['discription']}"
	event_records.append({"title": title, "start": row["date"], "end": row["end"]})

calendar_options = {
	"initialView": "dayGridMonth",
	"selectable": True
}
clicked = calendar(events=event_records, options=calendar_options, key="calendar")

with st.form("date_form"):
	name = st.text_input("Your Name")
	idea = st.text_input("What do you want to do on the date?")
	submit = st.form_submit_button("Book This Date")

	if submit and clicked and "start" in clicked and name:
		new_event = {
			"Name": name,
			"date": clicked["start"],
			"end": clicked["start"],
			"discription": idea
		}
		df = pd.concat([df, pd.DataFrame([new_event])], ignore_index=True)
		df.to_csv(csv_path, index=False)
		st.success(f"Date booked with Luuk on {clicked['start']}!")
		st.experimental_rerun()
