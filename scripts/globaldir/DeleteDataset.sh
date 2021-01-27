#!/bin/bash
#
# A script to prevent Michael from accidentally
# wiping out his filesystem

errorsig="Error: $(readlink -e $BASH_SOURCE)"

dataset=$1

if [[ "$1" == "" ]]; then
    echo "Please enter a dataset"
    exit
fi

if [[ $(readlink -e $dataset/data) != "" ]] &&  [[ $(readlink -e $dataset/PNG) != "" ]] && [[ $(readlink -e $dataset/metadata.toml) != "" ]]; then
    rm -rd $dataset
else
    echo $errorsig
    echo "Be careful! $dataset is not a dataset."
fi
