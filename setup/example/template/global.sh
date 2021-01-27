#!/bin/bash
#
#

# Set variable for location of this dataset
datapath=$(readlink -e -- $(dirname -- $BASH_SOURCE))

#
# SET PATH TO SOURCE INPUT DATA
#
sourcepath="SOURCE_PLACEHOLDER"
sourcepath=$(readlink -e $sourcepath)
sourcepaths="$SOURCEPATHS $sourcepath"

export SOURCEPATHS=$(echo $sourcepaths)

#
# SET PATH TO SETUP DATA
#
setuppath="SETUP_PLACEHOLDER"
setuppath=$(readlink -e $setuppath)
setuppaths="$SETUPPATHS $setuppath"

export SETUPPATHS=$(echo $setuppaths)
