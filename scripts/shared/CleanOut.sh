#!/bin/bash
#
# Clean .out scripts

sourcefn=$BASH_SOURCE
sourcedir=$(dirname -- $sourcefn)

cd $sourcedir
find . -mindepth 1 -maxdepth 1 -type f -name "*.out" -exec rm {} \;
cd -
