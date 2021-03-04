#!/bin/bash
#
# Convenience script to run all files in a certain class

sourcedir=$(dirname -- $BASH_SOURCE)

args=$@

source $sourcedir/local.sh

modules=($MODULES)
for module in "${modules[@]}"; do
    if [[ $args == *".toml"* ]]; then
	submit-script $args
    else
	$args
    fi
done
