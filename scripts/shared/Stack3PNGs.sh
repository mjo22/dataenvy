#!/bin/bash
#
# Template for stacking together plots from the same frames in 3 input directories

# Input parameters
input_path1="$1"
input_path2="$2"
input_path3="$3"

if [[ "$input_path1" == "" ]] || [[ "$input_path2" == "" ]] || [[ "$input_path3" == "" ]]; then
    echo "Enter two input paths of files, up until frame number"
    exit
fi

IFS='/' read -ra arr <<< "$input_path1"
input_basename1="${arr[-1]}"
IFS='/' read -ra arr <<< "$input_path2"
input_basename2="${arr[-1]}"
IFS='/' read -ra arr <<< "$input_path3"
input_basename3="${arr[-1]}"

input_directory1=$(dirname $input_path1)
input_directory2=$(dirname $input_path2)
input_directory3=$(dirname $input_path3)

# Output parameters
output_directory=./PNG

# Loop over directory. Expected that files end in "...FRAMENUMBER.png"
# and FRAMENUMBER is the only number in the filename.
for input_path1 in $input_directory1/${input_basename1}*.png; do
    input_file1="$(basename -- $input_path1)"
    temp="$(basename -- $input_file1 .png)"
    IFS='_' read -ra arr <<< "$temp"
    frame_number="${arr[-1]}"
    input_file2="${input_basename2}${frame_number}.png"
    input_path2="${input_directory2}/${input_file2}"
    input_file3="${input_basename3}${frame_number}.png"
    input_path3="${input_directory3}/${input_file3}"
    output_file="${input_basename1}${input_basename2}${input_basename3}${frame_number}.png"
    output_path="${output_directory}/${output_file}"
    echo "Writing frame ${frame_number}"
    ffmpeg -y -i $input_path1 -i $input_path2 -i $input_path3 -filter_complex "[0:v][1:v][2:v]hstack=inputs=3[v]" -map "[v]" $output_path
done
