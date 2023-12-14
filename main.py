from utils import load_wav2vec2_asr_model, transcribe_audio
import os
import sys
import speech_recognition

output_directory = "./output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
output_file = f'{output_directory}/{len(os.listdir(output_directory))}_transcript.txt'

def create_transcript(transcript_method):
    cleaned_audio_path = './audio/cleaned/cleaned_audio.wav'
    original_audio_path = './audio/original/audio_extracted.mp3'
    transcript = f'Speech to Text through {transcript_method}\n'

    if transcript_method == 'wav2vec':
        model_path = 'model.pth'
        model = load_wav2vec2_asr_model(model_path)

        audio_path = cleaned_audio_path
        temp = transcribe_audio(model, audio_path)
        transcript += f"Audio that has been cleaned: {temp}\n"

        audio_path = original_audio_path
        temp = transcribe_audio(model, audio_path)
        transcript += f"Audio that has not been cleaned: {temp}\n"

        return transcript
    
    r = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(cleaned_audio_path) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
            return text
        except:
            return "Could not recognize audio"
    
transcript_method = sys.argv[1]
with open(output_file, 'w+') as file:
    file.write(create_transcript(transcript_method))