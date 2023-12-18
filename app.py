import streamlit as st
import os
import zipfile
import shutil
import whisper
from moviepy.editor import *
import librosa
from pydub import AudioSegment
import noisereduce as nr
from scipy.io import wavfile
import streamlit_ext as ste


def extract_audio(video_path):
    output_directory = "./audio/original"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_path = f"{output_directory}/audio_extracted.mp3"

    video = VideoFileClip(str(video_path)) 
    audio = video.audio
    audio.write_audiofile(str(output_path))

def noise_removal():
    audio_path = './audio/original/audio_extracted.mp3'
    audio, sr = librosa.load(audio_path, sr=None)
    noise_reduced_audio = nr.reduce_noise(y=audio, sr=sr)
    output_directory = "./audio/cleaned"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    wavfile.write(f'{output_directory}/cleaned_audio.wav', sr, noise_reduced_audio)
    audio = AudioSegment.from_wav(f'{output_directory}/cleaned_audio.wav')
    audio.export(f'{output_directory}/cleaned_audio.mp3', format='mp3')

def generate_files(uploaded_file):
    video_path = "./temp_video.mp4"
    with open(video_path, "wb") as video_file:
        video_file.write(uploaded_file.read())
    st.video(video_path)
    st.write("Transcribing files. Please wait")
    extract_audio(video_path)
    noise_removal()
    try:
        model = whisper.load_model("base")
        result = model.transcribe("./audio/cleaned/cleaned_audio.mp3")["text"]
    except Exception as e:
        result = f"Error: Could not transcribe as {e}"
    output_directory = "./output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    with open('./output/whisper_transcript.txt', 'w+') as file:
        file.write(result)

    original_audio_path = './audio/original/audio_extracted.mp3'
    cleaned_audio_path = './audio/cleaned/cleaned_audio.mp3'
    with open('./output/whisper_transcript.txt', 'r') as file:
        transcript = file.read()

    os.remove(video_path)

    return original_audio_path, cleaned_audio_path, transcript

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1].lower() in {'mp4'}

def main():
    st.title("Transcribing Videos to Text")
    uploaded_file = st.file_uploader("Choose a video", type=["mp4"])
    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            original_audio, cleaned_audio, transcript = generate_files(uploaded_file)
            st.write("Original Audio file")
            st.audio(original_audio, format='audio/mp3', start_time=0)
            st.write("Cleaned Audio file")
            st.audio(cleaned_audio, format='audio/mp3', start_time=0)
            st.text_area("Transcribed Text", transcript)
            with zipfile.ZipFile('transcribed_files.zip', 'w') as zipf:
                zipf.write(original_audio, os.path.basename(original_audio))
                zipf.write(cleaned_audio, os.path.basename(cleaned_audio))
                zipf.write('./output/whisper_transcript.txt', 'transcript.txt')
            shutil.rmtree('./audio')
            shutil.rmtree('./output')
            with open('transcribed_files.zip', 'rb') as file:
                content = file.read()
            ste.download_button(label="Download Files", data=content, file_name='transcribed_files.zip')

if __name__ == "__main__":
    main()
