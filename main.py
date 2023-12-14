from utils import load_wav2vec2_asr_model, transcribe_audio

model_path = 'model.pth'
model = load_wav2vec2_asr_model(model_path)

audio_path = './audio/cleaned/cleaned_audio.wav'
temp = transcribe_audio(model, audio_path)
transcript = f"Audio that has been cleaned: {temp}\n"

audio_path = './audio/original/audio_extracted.mp3'
temp = transcribe_audio(model, audio_path)
transcript += f"Audio that has not been cleaned: {temp}\n"

output_file = './transcript.txt'
with open(output_file, 'w+') as file:
    file.write(transcript)