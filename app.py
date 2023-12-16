# Similar functionality as main.py, but for web app

from flask import Flask, render_template, request, send_from_directory
import os
import zipfile
import subprocess
from werkzeug.utils import secure_filename
import shutil
import whisper

app = Flask(__name__)

UPLOAD_FOLDER = './videos'
ALLOWED_EXTENSIONS = {'mp4'}
TRANSCRIPT_OUTPUT_FILE = './output/whisper_transcript.txt'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

def generate_files(video_path):
    gen_command = f"bash ./generate_transcripts.sh {video_path}"
    subprocess.run(gen_command, shell=True, capture_output=True, text=True)
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
    copy_command = f"bash ./copy_directory.sh"
    subprocess.run(copy_command, shell=True, capture_output=True, text=True)
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
    original_audio_path = './audio/original/audio_extracted.mp3'
    cleaned_audio_path = './audio/cleaned/cleaned_audio.mp3'
    transcript_path = './output/whisper_transcript.txt'

    with zipfile.ZipFile('generated_files.zip', 'w') as zipf:
        zipf.write(original_audio_path, os.path.basename(original_audio_path))
        zipf.write(cleaned_audio_path, os.path.basename(cleaned_audio_path))
        zipf.write(transcript_path, os.path.basename(transcript_path))

    # Cleaning up directories
    shutil.rmtree('./audio')
    shutil.rmtree('./output')
    shutil.rmtree('./graphs')
    shutil.rmtree('./static/audio')

    return send_from_directory('.', 'generated_files.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
