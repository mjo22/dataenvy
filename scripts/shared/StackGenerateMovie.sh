#!/bin/bash
#
# Stacking together plots, generate a movie, delete the stacked images

# Input parameters

orient=$1  # v or h
output_basename=$2  # base filename for output video and images
temp=($@)  # filepaths, up to frame number
input_paths=("${temp[@]:2}")
output_directory=./PNG

input_basenames=()
input_dirs=()
for input_path in "${input_paths[@]}"; do
    input_basename="$(basename -- $input_path)"
    input_basenames+=("$(basename -- $input_basename _)")
    input_dirs+=($(dirname -- $input_path))
done

nargs="${#input_dirs[@]}"
input_basename1="${input_basenames[0]}"
input_dir1="${input_dirs[0]}"
echo "$input_dir1/$input_basename1*.png"
for f in $input_dir1/$input_basename1*.png; do
    temp="$(basename -- $f .png)"
    IFS='_' read -ra arr <<< "$temp"
    frame="${arr[-1]}"
    inputargs=""
    filterargs=""
    for i in "${!input_dirs[@]}"; do
	    dir="${input_dirs[$i]}"
	    input_basename="${input_basenames[$i]}"
	    inputargs="${inputargs}-i ${dir}/${input_basename}_${frame}.png "
	    filterargs="${filterargs}[$i:v]"
    done
    outputpath="${output_directory}/${output_basename}"
    echo "Writing frame ${frame}"
    ffmpeg -y $inputargs -filter_complex "${filterargs}${orient}stack=inputs=${nargs}[v]" -map "[v]" "${outputpath}_${frame}.png" -loglevel warning
done

bash GenerateMovie.sh $outputpath

#rm $outputpath*.png
