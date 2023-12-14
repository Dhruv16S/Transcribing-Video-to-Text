import sys
from moviepy.editor import *
import os

output_directory = "./audio/original"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
output_path = f"{output_directory}/audio_extracted.mp3"

print(f"Input video: {sys.argv[1]}")
video = VideoFileClip(str(sys.argv[1])) 
audio = video.audio
audio.write_audiofile(str(output_path))