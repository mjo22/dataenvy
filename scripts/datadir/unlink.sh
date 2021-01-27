#!/bin/bash
#
# Remove all hyperlinks in dataset

sourcedir=$(dirname -- $BASH_SOURCE)

find -L $sourcedir -xtype l -delete
