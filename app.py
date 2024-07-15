import streamlit as st

st.title("Earthlings Music")
st.write("Welcome to the Earthlings Music app!")

# Simple text input
name = st.text_input("What's your name?")
st.write(f"Hello, {name}!")

# Simple slider for selecting a number
number = st.slider("Pick a number", 0, 100)
st.write(f"You picked: {number}")

# Display a sample music link
st.write("Here is a sample music track:")
st.audio("https://www.sample-videos.com/audio/mp3/crowd-cheering.mp3")
