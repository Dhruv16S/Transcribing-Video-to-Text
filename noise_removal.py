import librosa
from pydub import AudioSegment
import os
from plots import *
import noisereduce as nr
from scipy.io import wavfile


audio_path = './audio/original/audio_extracted.mp3'
audio, sr = librosa.load(audio_path, sr=None)

noise_reduced_audio = nr.reduce_noise(y=audio, sr=sr)

output_directory = "./graphs/cleaned"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

plot_audio(noise_reduced_audio, sr, output_directory, title='Cleaned_Audio')
plot_spectrogram(noise_reduced_audio, sr, output_directory, title='Cleaned_Audio_Spectrogram')

output_directory = "./audio/cleaned"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

wavfile.write(f'{output_directory}/cleaned_audio.wav', sr, noise_reduced_audio)

audio = AudioSegment.from_wav(f'{output_directory}/cleaned_audio.wav')
audio.export(f'{output_directory}/cleaned_audio.mp3', format='mp3')
