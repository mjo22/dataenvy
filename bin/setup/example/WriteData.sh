#!/bin/bash
#
# Script that writes data from some input into a dataset!

if [ "$1" = "" ] || [ "$2" = "" ]; then
    echo "Enter input and output data directories"
    exit
fi

# Check that input and output directories exist
inputpath=$(readlink -e $1)
outputpath=$(readlink -e $2)

if [[ "$inputpath" == "" ]]; then
    echo $errorsig
    echo "Input path $1 does not exist"
    exit
fi
if [[ "$outputpath" == "" ]]; then
    echo $errorsig
    echo "Output path $2 does not exist"
    exit
fi

# Write metadata
cd $outputpath/..
python write_metadata.py
cd -

# Write data
