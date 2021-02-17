#!/bin/bash
#
# Convenience script to run all files in a certain class

sourcedir=$(dirname -- $BASH_SOURCE)
errorsig="ERROR: $BASH_SOURCE"
label=$1

temp=($@)
args="${temp[@]:1}"

if [[ $label == "" ]]; then
    echo $errorsig
    echo "Please enter a label for the file class"
    exit
fi

find -L $sourcedir -maxdepth 1 -mindepth 1 -name "${label}*.toml" -xtype l -exec bash $sourcedir/Run.sh $sourcedir/${label}.py {} $args \;

find $sourcedir -maxdepth 1 -mindepth 1 -name "${label}*.toml" -type f -exec bash $sourcedir/Run.sh $sourcedir/${label}.py {} $args \;
