# Similar functionality as main.py, but for web app

from flask import Flask, render_template, request, send_from_directory
import os
import zipfile
import subprocess
from werkzeug.utils import secure_filename
import shutil
import whisper
from moviepy.editor import *
import librosa
from pydub import AudioSegment
import noisereduce as nr
from scipy.io import wavfile

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

app = Flask(__name__)

UPLOAD_FOLDER = './videos'
ALLOWED_EXTENSIONS = {'mp4'}
TRANSCRIPT_OUTPUT_FILE = './output/whisper_transcript.txt'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

def generate_files(video_path):

    # gen_command = f"bash ./generate_transcripts.sh {video_path}"
    # subprocess.run(gen_command, shell=True, capture_output=True, text=True)
    # Python implementation of above codes
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
    with open(TRANSCRIPT_OUTPUT_FILE, 'w+') as file:
        file.write(result)

    # copy_command = f"bash ./copy_directory.sh"
    # subprocess.run(copy_command, shell=True, capture_output=True, text=True)
    shutil.move('./audio', './static/')

    original_audio_path = 'static/audio/original/audio_extracted.mp3'
    cleaned_audio_path = 'static/audio/cleaned/cleaned_audio.mp3'
    with open('./output/whisper_transcript.txt', 'r') as file:
        transcript = file.read()

    return original_audio_path, cleaned_audio_path, transcript

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', original_audio=None,
                                   cleaned_audio=None, transcript=None)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    output_directory = "./videos"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if request.method == 'POST':
        file = request.files['formFile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = f"{UPLOAD_FOLDER}/{filename}"
            file.save(file_path)

            original_audio, cleaned_audio, transcript = generate_files(file_path)

            if os.path.exists(UPLOAD_FOLDER):
                for item in os.listdir(UPLOAD_FOLDER):
                    item_path = os.path.join(UPLOAD_FOLDER, item)
                    os.remove(item_path)

            return render_template('index.html', original_audio=original_audio,
                                   cleaned_audio=cleaned_audio, transcript=transcript)

    return render_template('index.html', original_audio=None,
                                   cleaned_audio=None, transcript=None)

@app.route('/download', methods=['GET'])
def download():
    original_audio_path = './static/audio/original/audio_extracted.mp3'
    cleaned_audio_path = './static/audio/cleaned/cleaned_audio.mp3'
    transcript_path = './output/whisper_transcript.txt'

    with zipfile.ZipFile('generated_files.zip', 'w') as zipf:
        zipf.write(original_audio_path, os.path.basename(original_audio_path))
        zipf.write(cleaned_audio_path, os.path.basename(cleaned_audio_path))
        zipf.write(transcript_path, os.path.basename(transcript_path))

    # Cleaning up directories
    shutil.rmtree('./videos')
    shutil.rmtree('./output')
    shutil.rmtree('./static/audio')

    return send_from_directory('.', 'generated_files.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
