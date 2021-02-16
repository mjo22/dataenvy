#!/bin/bash
#
# Submission for python script

sourcefn=$BASH_SOURCE
errorsig="ERROR: $sourcefn"
sourcedir=$(readlink -e $(dirname -- $sourcefn))

# Unpack args for python
pyscript=$1
pyconfig=$2
where=${3:-"nohup"}

# Slurm args
temp=($@)
args="${temp[@]:3}"

# Configure if running from a dataset
if [ -f "$sourcedir/metadata.toml" ]; then
    source $sourcedir/local.sh
elif [ -f "$sourcedir/../metadata.toml" ]; then
    source $sourcedir/../local.sh
fi

# Check if script and config exist
if [[ ! -f $pyscript ]]; then
    echo $errorsig
    echo "$pyscript does not exist"
    exit
fi
if [[ ! -f $pyconfig ]]; then
    echo $errorsig
    echo "$pyconfig does not exist"
    exit
fi

# Run
if [[ $where == "nohup" ]]; then
    rm nohup.out
    nohup python $pyscript $pyconfig &
elif [[ $where == "local" ]]; then
    python $pyscript $pyconfig
elif [[ $where == "slurm" ]]; then
    sbatch $args $pyscript $pyconfig
else
    echo $errorsig
    echo "$where option is not supported"
    exit
fi
