#!/bin/bash

sourcefn=$(readlink -e $BASH_SOURCE)
errorsig="ERROR: sourcefn"

name="$1"

if [[ $name = "" ]]; then
    echo "Missing argument: input a name for new module."
    exit
fi

outdir=$DATAENVY/modules/$name

if [[ -d "$outdir" ]]; then
    echo "Directory $outdir already exists. Please delete directory and try again."
    exit
else
    mkdir $outdir
fi

echo "Copying module template to ${outdir}..."

cp -r $DATAENVY/modules/template/* $outdir

echo "Renaming placeholder names..."

find $outdir -name "PLACEHOLDER*" -type f -exec rename "PLACEHOLDER" "${name}" {} ";"

echo "Replacing placeholder text..."

find $outdir -maxdepth 1 -type f -exec sed -i s:PLACEHOLDER:$name:g {} \;

if [[ -d "$DATAENVY/scripts/datadir/$name" ]]; then
    rm -rd $DATAENVY/scripts/datadir/$name
    rm -rd $DATAENVY/scripts/globaldir/$name
    rm -rd $DATAENVY/scripts/shared/$name
else
    mkdir $DATAENVY/scripts/datadir/$name
    mkdir $DATAENVY/scripts/globaldir/$name
    mkdir $DATAENVY/scripts/shared/$name
fi
