#!/bin/bash
#
#

# Set variable for location of this dataset
datapath=$(readlink -e -- $(dirname -- $BASH_SOURCE))

# Set location of setup directory
temp="PLACEHOLDER"
setuppath=$(readlink -e -- $temp)
if [[ "$setuppath" == "" ]]; then
    echo "$errorsig"
    echo "Setup directory $temp could not be found"
    exit
fi

# Configure dataset type
source $setuppath/Config.sh
