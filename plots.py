import librosa
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_audio(audio, sr, output_directory, title):
    time = np.arange(0, len(audio)) / sr
    plt.plot(time, audio)
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.savefig(f'{output_directory}/{title}.png')
    plt.close()

def plot_spectrogram(audio, sr, output_directory, title):
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(log_spectrogram, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title(title)
    plt.savefig(f'{output_directory}/{title}_extracted_audio.png')
    plt.close()