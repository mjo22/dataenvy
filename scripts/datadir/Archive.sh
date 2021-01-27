#!/bin/bash
#
# Archive dataset by turning all symlinks to original files

sourcefn=$BASH_SOURCE
sourcedir=$(dirname -- $sourcefn)
errorsig="ERROR: $sourcefn"

# Make sure we are running this script from a dataset
if [ ! -d $PWD/data ] || [ ! -f $PWD/metadata.toml ]; then
    echo $errorsig
    echo "Be careful! Working directory does not seem to be a dataset."
    exit
fi

for f in $(find -L $sourcedir -xtype l); do
    cp --remove-destination $(readlink $f) $f
done
