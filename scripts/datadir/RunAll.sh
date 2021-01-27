#!/bin/bash
#
# Convenience script to run all files in a certain class

sourcedir=$(dirname -- $BASH_SOURCE)
label=$1

temp=($@)
args="${temp[@]:1}"

if [[ $label == "" ]]; then
    echo "Please enter a label for the file class"
    exit
fi

source $sourcedir/local.sh

modules=($MODULES)
for module in "${modules[@]}"; do
    find -L $sourcedir/$module -maxdepth 1 -mindepth 1 -name "${label}*.toml" -xtype l -exec bash $sourcedir/$module/Run.sh $sourcedir/$module/${label}Data.py {} $args \;
done
