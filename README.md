# Introduction

The following repository is the first among a series of repositories that can read an audio file and transliterate the source language to another target language. The system `Transcribing Video to Text` takes a video file as an input and generates two audio files and a transcript of the audio in a .txt format. The first audio file is the actual audio from the video, while the second file is an audio without the background sounds or any noise.

The working of the system is as follows. The video file (.mp4) passed as an input is used to separate the audio and visual streams. The [MoviePy](https://pypi.org/project/moviepy/) python package is used for this purpose. The background sounds and noise are eliminated through [Denoising Methods](https://ankurdhuriya.medium.com/audio-enhancement-and-denoising-methods-3644f0cad85b) and [Spectral Gating](https://pypi.org/project/noisereduce/). Finally the [Wav2Vec2](https://pytorch.org/audio/stable/tutorials/speech_recognition_pipeline_tutorial.html#overview) and [Whisper](https://github.com/openai/whisper) models are used to convert speech to text, thereby accomplishing transcription.


## Clone the repository

```
git clone https://github.com/Dhruv16S/Transcribing-Video-to-Text.git
```

## Create a virtual environment (optional)

```
virtualenv env
source env/scripts/activate
```

## Download requirements

```
pip install -r requirements.txt
```

## Download requirements

Download suitable PyTorch version from [here](https://pytorch.org/get-started/locally/). The following cmd worked for me
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Create a directory

In your project directory, create a new folder

```
mkdir videos
```
Add all your video files in this directory.

## Run the application through CLI

`Note:` Before using the wav2vec model, run the `model.ipynb` file.

```
./generate_transcripts.sh <video_file_path> <transcription_method>
```
Example cmd:
```
./generate_transcripts.sh ./videos/input_video.mp4 whisper
```

`<video_file_path>:` Mention the path of your video file here.
`<transcription_method>: (optional)` Mention which model must be used for speech to text. (wav2vec or whisper). Use this parameter to generate transcripts, otherwise only the audio files will be generated.

The generated audio files can be found in `./audio` and the transcripts can be found under `./output` directories.