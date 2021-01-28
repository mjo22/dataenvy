#!/bin/bash
#
# Convenience script to run all files in a certain class

sourcedir=$(dirname -- $BASH_SOURCE)

temp=($@)

source $sourcedir/local.sh

modules=($MODULES)
for module in "${modules[@]}"; do
    bash $sourcedir/$module/RunAll.sh $args
done
