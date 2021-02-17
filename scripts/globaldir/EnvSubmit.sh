#!/bin/bash
#
# Submission script for many scripts shared in each dataset

sourcefn=$BASH_SOURCE
errorsig="ERROR: $sourcefn"
sourcedir=$(readlink -e $(dirname -- $sourcefn))

datapaths=($DATAPATHS)

Script=$1

temp=($@)
args="${temp[@]:1}"

for datapath in "${datapaths[@]}"; do

    cd $datapath

    source local.sh

    bash $Script $args

    cd -
    
done
