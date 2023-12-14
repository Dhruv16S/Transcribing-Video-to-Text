#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_audio_file>"
    exit 1
fi
input_argument="$1"
python extract_audio.py "$input_argument"