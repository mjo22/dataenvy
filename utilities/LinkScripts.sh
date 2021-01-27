#!/bin/bash
#
# Links specified scripts to some data directory

if [[ "$1" == "" ]] || [[ "$2" == "" ]]; then
    echo "Specify input and output directories for linking"
    exit
fi

errorsig="ERROR: $BASH_SOURCE"

script_directory=$(readlink -e "$1")
data_directory=$(readlink -e "$2")

if [[ "$script_directory" == "" ]]; then
    echo "$errorsig"
    echo "Input directory $1 could not be found"
    exit
fi

if [[ "$data_directory" == "" ]]; then
    echo "$errorsig"
    echo "Data directory $2 could not be found"
    exit
fi

# Link files (not directories in folder to data directory)
for path in $script_directory/*; do
    if [[ -d "$path" ]]; then
	continue
    elif [[ -f "$path" ]]; then
	file="$(basename -- $path)"
	if [[ "$file" != *~* ]] && [[ "$file" != '*' ]] && [[ "$file" != *#* ]]; then
	    ln -s "$path" "$data_directory/$file"
	fi
    fi
done
