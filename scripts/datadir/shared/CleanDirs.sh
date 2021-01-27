#!/bin/bash
#
# Cleans directories of all contents but metadata

sourcefn=$BASH_SOURCE
sourcedir=$(dirname -- $sourcefn)
errorsig="ERROR: $sourcefn"

dirs=($@)
expanded=()
for dir in "${dirs[@]}"; do
    for d in $dir; do
	expanded+=($d)
    done
done

for dir in "${expanded[@]}"; do
    if [ ! -d $dir ]; then
	echo $errorsig
	echo "Directory $dir does not exist"
	exit
    fi
    find $dir ! -name 'metadata.toml' -type f -exec rm {} +
done
