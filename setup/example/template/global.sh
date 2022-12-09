#!/bin/bash

# Set location of this dataset
datapath=$(readlink -e -- $(dirname -- $BASH_SOURCE))
datapaths="$DATAPATHS $datapath"

export DATAPATHS=$(echo $datapaths)

# Set path to source input data
setuppath="SETUP_PLACEHOLDER"
setuppaths="$SETUPPATHS $setuppath"

export SETUPPATHS=$(echo $setuppaths)

# Set path to setup folder
sourcepath="SOURCE_PLACEHOLDER"
sourcepaths="$SOURCEPATHS $sourcepath"

export SOURCEPATHS=$(echo $sourcepaths)

# Configure, assuming all datasets will set the same variables.
source $setuppath/Config.sh
