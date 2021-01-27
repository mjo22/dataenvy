#!/bin/bash

sourcefn=$(readlink -e $BASH_SOURCE)
errorsig="ERROR: sourcefn"

name="$1"

if [[ $name = "" ]]; then
    echo "Missing argument: input a name for new module."
    exit
fi

echo "Copying module template to ${name}..."

cp -r template $name

echo "Renaming placeholder names..."

find ./$name -name "GREENELEPHANT*" -exec rename "GREENELEPHANT" "${name}" {} ";"

echo "Replacing placeholder text..."

find ./$name -maxdepth 1 -type f -exec sed -i s:GREENELEPHANT:$name:g {} \;

mkdir $DATAENVY/scripts/datadir/$name
mkdir $DATAENVY/scripts/globaldir/$name
mkdir $DATAENVY/scripts/shared/$name

touch $DATAENVY/scripts/datadir/$name/.gitkeep
touch $DATAENVY/scripts/globaldir/$name/.gitkeep
touch $DATAENVY/scripts/shared/$name/.gitkeep
