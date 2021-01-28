#!/bin/bash
#
#

# Path to this file
sourcefn=$(readlink -e -- $BASH_SOURCE)
sourcedir=$(dirname -- $sourcefn)
errorsig="ERROR: $sourcefn"

if [[ "$1" == "" ]] || [[ "$2" == "" ]] || [[ "3" == "" ]] ; then
    echo "Enter input, output, and setup directories"
    exit
fi

# Gather input and output directories
inputpath=$(readlink -e $1)
outputpath=$2
setuppath=$(readlink -e $3)
probeoutput=$(readlink -e $outputpath)

# Check args
if [[ "$inputpath" == "" ]]; then
    echo $errorsig
    echo "Input path $1 does not exist"
    exit
fi

if [[ "$probeoutput" != "" ]]; then
    echo "Output path $outputpath exists. Deleting..."
    bash DeleteDataset.sh $outputpath
fi

if [[ "$setuppath" == "" ]]; then
    echo $errorsig
    echo "Setup path $3 does not exist"
    exit
fi

# Create dataset
rsync -a --exclude '*~' $setuppath/template/* $outputpath

# Get setuppath in terms of $DATAENVY
cut=${setuppath#"$DATAENVY"}
setupliteral="\$DATAENVY$cut"

# Add source data path and setup path to global.sh
sed -i "s:SOURCE_PLACEHOLDER:$inputpath:g" $outputpath/global.sh
sed -i "s:SETUP_PLACEHOLDER:$setupliteral:g" $outputpath/global.sh

# Add setup source directory to local.sh
sed -i "s:PLACEHOLDER:$setupliteral:g" $outputpath/local.sh

# Add setup source directory to link.sh
sed -i "s:PLACEHOLDER:$setupliteral:g" $outputpath/link.sh

# Add source data path to write_metadata.py
sed -i "s:PLACEHOLDER:$inputpath:g" $outputpath/write_metadata.py

# Configure modules
source $outputpath/local.sh

# Create analysis directories
modules=($MODULES)
for module in ${modules[@]}; do
    mkdir $outputpath/$module
    mkdir $outputpath/$module/result
    mkdir $outputpath/$module/PNG
done

# Run linkage
source $outputpath/link.sh

# Write data
bash $setuppath/WriteData.sh $inputpath $outputpath/data

# Write modules
bash $outputpath/RunAll.sh Write local INFO

# Create plots
bash $outputpath/RunAll.sh Plot local INFO

# Goodbye!
echo "Setup complete."
