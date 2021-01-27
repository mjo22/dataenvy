#!/bin/bash
#
# A template for writing a folder of .pngs to a movie with ffmpeg

# Input variables. Enter everything up to frame numbers in input directory
input_basename="$1"

if [[ "$input_basename" == "" ]]; then
    echo "Enter the name of the files to compile, up until the frame number"
    exit
fi

input_directory="$(dirname -- $input_basename)"
input_basename="$(basename -- $input_basename)"
IFS='_' read -ra arr <<< "$input_basename"
input_basename="$(basename -- $input_basename _)"

# Output variables
output_directory=${2:-"$input_directory"}
output_basename=$input_basename

# FFMPEG parameters
fps=4
ffmpeg -f image2 -framerate $fps -i $input_directory/$input_basename%*.png -vcodec libx264 -pix_fmt yuv420p -y $output_directory/$output_basename.mp4
