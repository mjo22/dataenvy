#!/bin/bash
#
# Submission script for many python scripts shared in each dataset

sourcefn=$BASH_SOURCE
errorsig="ERROR: $sourcefn"
sourcedir=$(readlink -e $(dirname -- $sourcefn))

datapaths=($DATAPATHS)

pyscript=$1
pyconfig=$2

temp=($@)
args="${temp[@]:2}"

for datapath in "${datapaths[@]}"; do

    cd $datapath

    source local.sh

    modules=($MODULES)
    for module in "${modules[@]}"; do
	if [ -f $module/$pyconfig ]; then
	    bash $module/Run.sh $module/$pyscript $module/$pyconfig $args
	fi
    done

    cd -
    
done
