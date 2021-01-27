#!/bin/bash
#
# Clean slurm and nohup scripts

find . -mindepth 1 -maxdepth 1 -type f -name "slurm-*.out" -exec rm {} \;
find . -mindepth 1 -maxdepth 1 -type f -name "nohup*.out" -exec rm {} \;
