#!/bin/bash
#
# Configuration file for setting up dataset

# Set location of current dataset
datapath="$(dirname $BASH_SOURCE)"

# Configure environment
source $datapath/local.sh

# Error signature
errorsig="ERROR: $BASH_SOURCE"

# Set location of setup directory
temp="PLACEHOLDER"
setuppath=$(readlink -e -- $temp)
if [[ "$setuppath" == "" ]]; then
    echo "$errorsig"
    echo "Setup directory $temp could not be found"
    exit
fi

# Set location of global linking file
temp="$DATAENVY/utilities/LinkDataset.sh"
linkfile=$(readlink -e -- $temp)

if [[ "$linkfile" == "" ]]; then
    echo "$errorsig"
    echo "Linking file $temp could not be found"
    exit
fi

bash $linkfile $datapath $setuppath
