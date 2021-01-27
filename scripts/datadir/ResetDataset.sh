#!/bin/bash
#
#
# Resets contents of dataset

sourcedir=$(dirname $BASH_SOURCE)

source $sourcedir/local.sh

modules=($MODULES)
for module in "${modules[@]}"; do
    cd $sourcedir/$module
    bash CleanDirs.sh result* PNG
    cd -
done

bash $sourcedir/unlink.sh
bash $sourcedir/link.sh
