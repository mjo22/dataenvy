#!/bin/bash
#
# Link scripts to global directory for data comparison

sourcefn=$(readlink -e -- "$BASH_SOURCE")
errorsig="ERROR: $sourcefn"

if [[ "$1" == "" ]] || [[ "$2" == "" ]]; then
    echo "Please enter a directory and the type of dataset"
    exit
fi

workingdir=$(readlink -e $1)

if [[ "$workingdir" == "" ]]; then
    echo $errorsig
    echo "Directory $1 could not be found"
    exit
fi

temp="$DATAENVY/modules/$2.sh"
modulesrc=$(readlink -e $temp)

if [[ "$modulesrc" == "" ]]; then
    echo $errorsig
    echo "Module source $temp could not be found"
    exit
fi

temp="$DATAENVY/utilities/LinkScripts.sh"
linker=$(readlink -e "$temp")

if [[ "$linker" == "" ]]; then
    echo $errorsig
    echo "Linking script $temp could not be found"
    exit
fi

# Set module settings
source $modulesrc

# Remove broken links
find -L $workingdir -mindepth 1 -maxdepth 1 -type l -delete

# Link utilities
temps=("$DATAENVY/scripts/globaldir" "$DATAENVY/scripts/shared")
dirs=()
for temp in "${temps[@]}"; do
    dir=$(readlink -e $temp)
    if [[ "$dir" == "" ]]; then
	echo $errorsig
	echo "Script directory $temp could not be found"
	exit
    fi
    bash $linker $dir $workingdir
    dirs+=("$dir")
done

# Link scripts that operate across datasets
modules=($MODULES)
for module in "${modules[@]}"; do
    for dir in "${dirs[@]}"; do
	temp="$dir/$module"
	moddir=$(readlink -e $temp)
	if [[ "$moddir" == "" ]]; then
	    echo $errorsig
	    echo "Module directory $temp could not be found"
	    exit 
	fi
	bash $linker $moddir $workingdir
	done
done
