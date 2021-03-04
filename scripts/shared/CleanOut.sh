#!/bin/bash
#
# Clean .out scripts

find . -mindepth 1 -maxdepth 1 -type f -name "*.out" -exec rm {} \;
