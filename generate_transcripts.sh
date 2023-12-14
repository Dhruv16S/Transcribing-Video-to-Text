#!/bin/bash
if [ "$#" -ne 2 ]
then
    echo "Usage: $0 <path_to_audio_file> <transcription_method>"
    echo "<transcription_method>: asr or wav2vec"
    exit 1
fi

if [ "$2" != "asr" ] && [ "$2" != "wav2vec" ]
then
    echo "Invalid transcription method. Please choose 'asr' or 'wav2vec'."
    echo "Usage: $0 <path_to_audio_file> <transcription_method>"
    exit 1
else
    transcript_method="$2"
fi

input_file="$1"
python extract_audio.py "$input_file"
python preprocess_audio.py
echo "Preprocessing complete"
python noise_removal.py
echo "Noise removal complete"
python main.py "$transcript_method"
echo "Transcript generation complete"