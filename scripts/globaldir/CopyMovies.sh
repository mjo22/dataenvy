#!/bin/bash
#
# Copy movies to home directory

moviedir=$1

if [[ $1 == "" ]]; then
    echo "Please enter a directory name"
    exit
fi

if [ ! -d $moviedir ]; then
    mkdir $moviedir
fi

cp $GLOBALDIR/PNG/*.mp4 $moviedir

#datapaths=($DATAPATHS)
#for datapath in "${datapaths[@]}"; do
#    dataset=$(basename -- $datapath)
#    dir=$moviedir/$dataset
#    if [ ! -d $dir ]; then
#	mkdir $dir
#    fi
#    rsync $datapath/PNG/*.mp4 $dir
#done
