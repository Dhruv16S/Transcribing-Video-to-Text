import streamlit as st
import requests

st.title("Transcribing Video to Text")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
if uploaded_file:
    files = {"formFile": uploaded_file}
    response = requests.post("http://localhost:5000/generate", files=files)
    result = response.json() 
    st.audio(result["original_audio"], format="audio/mp3", start_time=0)
    st.audio(result["cleaned_audio"], format="audio/mp3", start_time=0)
    st.text(result["transcript"])
