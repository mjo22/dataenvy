#!/bin/bash
#
# Submission for python script

sourcefn=$BASH_SOURCE
errorsig="ERROR: $sourcefn"
sourcedir=$(readlink -e $(dirname -- $sourcefn))

pyscript=$1
pyconfig=$2
where=${3:-"nohup"}
log=${4:-"INFO"}

if [ -f "$sourcedir/metadata.toml" ]; then
    cfg=$sourcedir/local.sh
else
    cfg=$sourcedir/../local.sh
fi

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
if [[ -f $cfg ]]; then
    source $cfg
    source $DATAENVY/configenvy "$(dirname -- $cfg)"
fi


if [[ $where == "nohup" ]]; then
    rm nohup.out
    nohup python $pyscript $pyconfig --log=$log &
elif [[ $where == "local" ]]; then
    python $pyscript $pyconfig --log=$log
elif [[ $where == "cpu" ]]; then
    sbatch -p ccb $pyscript $pyconfig --log=$log
elif [[ $where == "gpu" ]]; then
    sbatch -p gpu --gpus=a100-40gb:1 --cpus-per-gpu=8 --time=600 $pyscript $pyconfig --log=$log
else
    echo $errorsig
    echo "$where option is not supported"
    exit
fi
