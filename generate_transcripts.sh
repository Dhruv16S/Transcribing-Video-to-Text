#!/bin/bash
if [ "$#" -gt 2 ] || [ "$#" -eq 0 ]
then
    echo "Usage: $0 <path_to_audio_file> <transcription_method>(optional)"
    echo "<transcription_method>: whisper or wav2vec"
    exit 1
fi

if [ "$#" -eq 1 ]
then
    input_file="$1"
    python extract_audio.py "$input_file"
    python preprocess_audio.py
    echo "Preprocessing complete"
    python noise_removal.py
    echo "Noise removal complete"
else
    if [ "$2" != "whisper" ] && [ "$2" != "wav2vec" ]
    then
        printf "\nInvalid transcription method. Please choose 'whisper' or 'wav2vec'.\n"
        printf "Usage: $0 <path_to_audio_file> <transcription_method>(optional)\n\n"
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
fi