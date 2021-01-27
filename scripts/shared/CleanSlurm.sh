#!/bin/bash
#
# Clean slurm and nohup scripts

find . -type f -name "slurm-*.out" -exec rm {} \;
find . -type f -name "nohup.out" -exec rm {} \;
