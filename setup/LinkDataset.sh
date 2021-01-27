#!/bin/bash
#
# Links relevant analysis scripts to datasets

if [[ "$1" == "" ]] || [[ "$2" == "" ]]; then
    echo "Enter data directory, setup directory, and script directory name."
    exit
fi

# Set location of source directory
sourcedir=$(readlink -e -- $(dirname -- "$BASH_SOURCE"))

# Error signature
errorsig="ERROR: $BASH_SOURCE"

# Set location of dataset
datapath=$(readlink -e -- "$1")
if [[ "$datapath" == "" ]]; then
    echo $errorsig
    echo "Data directory $1 could not be found"
    exit
fi

# Set location of setup
setuppath=$(readlink -e -- "$2")
if [[ "$setuppath" == "" ]]; then
    echo $errorsig
    echo "Setup directory $2 could not be found"
    exit
fi

#
# Remove broken symlinks 
#
find -L $datapath -type l -delete

#
# LINK METADATA TO DIRECTORIES
#

# Check existance of metadata
temp="$datapath/metadata.toml"
metadata=$(readlink -e $temp)
if [[ "$metadata" == "" ]]; then
    echo $errorsig
    echo "Metadata file $temp could not be found"
    exit
fi

# Link metadata to data directory
temp="$datapath/data"
dir=$(readlink -e "$temp")
if [[ "$dir" == "" ]]; then
    echo $errorsig
    echo "Data directory $temp could not be found"
    exit
fi
ln -s $metadata $dir

# Create new module directories if does not exist
modules=($MODULES)
for module in "${modules[@]}"; do
    moddir="$datapath/$module"
    if [ ! -d $moddir ]; then
	mkdir $moddir
	mkdir $moddir/result
	mkdir $moddir/PNG
    fi
done

# Link metadata to result directories
modules=($MODULES)
for module in "${modules[@]}"; do
    temp="$datapath/$module/result"
    dir=$(readlink -e "$temp")
    if [[ "$dir" == "" ]]; then
	echo $errorsig
	echo "Result directory $temp could not be found"
	exit
    fi
    for resultdir in $dir*; do
	ln -s $metadata $resultdir
    done
done

#
# LINK SCRIPTS TO FOLDER
#

# Get linking script
temp=$DATAENVY/utilities/LinkScripts.sh
linker=$(readlink -e $temp)
if [[ "$linker" == "" ]]; then
    echo $errorsig
    echo "Linking script $temp could not be found"
    exit
fi

#  Link non-module scripts to data path
temps=("$DATAENVY/scripts/datadir" "$DATAENVY/scripts/shared" "$setuppath/scripts")
dirs=()
for temp in "${temps[@]}"; do
    dir=$(readlink -e $temp)
    if [[ "$dir" == "" ]]; then
	echo $errorsig
	echo "Directory $temp could not be found"
	exit
    fi
    bash $linker $dir $datapath
    dirs+=("$dir")
done

datadir="${dirs[0]}"
shareddir="${dirs[1]}"
setupdir="${dirs[2]}"

for module in "${modules[@]}"; do

    temp=$datapath/$module
    outputdir=$(readlink -e $temp)
    
    if [[ "$outputdir" == "" ]]; then
	echo $errorsig
	echo "Output directory $temp could not be found"
	exit
    fi
    
    dirs=("$datadir/shared" "$shareddir")
    dirs+=("$datadir/$module" "$shareddir/$module" "$setupdir/$module")

    for temp in "${dirs[@]}"; do
	dir=$(readlink -e $temp)
	if [[ "$dir" == "" ]]; then
	    echo $errorsig
	    echo "Input directory $temp could not be found"
	    exit
	fi
	bash $linker $dir $outputdir
    done
    
done
