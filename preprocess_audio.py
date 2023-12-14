import librosa
from plots import *
import os

audio_path = './audio/original/audio_extracted.mp3'
audio, sr = librosa.load(audio_path, sr=None)

output_directory = "./graphs/original"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

plot_audio(audio, sr, output_directory, title='Original Audio')
normalized_audio = librosa.util.normalize(audio)
plot_audio(normalized_audio, sr, output_directory, title='Normalized Audio')
plot_spectrogram(audio, sr, output_directory, title='Spectrogram')