import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from streamlit_calendar import calendar


# Functions
def load_data(path):
    df = pd.read_csv(path)
    return df



# Main_streamlit shit
st.title("📊 Scouting Dating")

st.write("Welcome to my app! Enter your name:")

name = st.text_input("Name:")

if name:
    st.success(f"Hello, {name}! You want to submit yourself for a date?")

st.title("📅 Clickable Calendar")

df = pd.read_csv('Data_files/Luuk_data.csv')

events = []
for _, row in df.iterrows():
    events.append({
        "title": row["Name"],
        "start": row["date"],
        "end": row["end"],
    })


default = {
    "initialView": "dayGridMonth",
    "editable": True,
    "selectable": True,
}

clicked = calendar(events=events, options=default)

if clicked:
    st.write("Clicked Event or Date:")
    st.json(clicked)