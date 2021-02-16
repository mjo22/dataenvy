#!/bin/bash

# Set location of this dataset
datapath=$(readlink -e -- $(dirname -- $BASH_SOURCE))
export DATAPATHS=$(echo $datapath)

# Set path to setup folder
setuppath="SETUP_PLACEHOLDER"
export SETUPPATHS=$(echo $setuppath)

# Set path to source input data
sourcepath="SOURCE_PLACEHOLDER"
export SOURCEPATHS=$(echo $sourcepath)

# Configure
source $setuppath/Config.sh
