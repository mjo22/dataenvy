#!/bin/bash
#
#

# Path to this file
sourcefn=$(readlink -e -- $BASH_SOURCE)
sourcedir=$(dirname -- $sourcefn)
errorsig="ERROR: $sourcefn"

if [[ "$1" == "" ]] || [[ "$2" == "" ]] ; then
    echo "Enter output and setup directories"
    exit
fi

# Gather input and output directories
inputpath=$(readlink -e $1)
setuppath=$(readlink -e $3)

# Check args
if [[ "$inputpath" == "" ]]; then
    echo $errorsig
    echo "Input path $1 does not exist"
    exit
fi

if [[ "$setuppath" == "" ]]; then
    echo $errorsig
    echo "Setup path $3 does not exist"
    exit
fi

# Create dataset
rsync -ua --progress $setuppath/template $outputpath
