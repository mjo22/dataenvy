#!/bin/bash
#
# Make scripts into executables


commands=("setup-global" "setup-datasets" "setup-dataset" "sync-dataset" "write-dataset" "delete-dataset" "submit-script" "submit-modules" "submit-base")

for cmd in "${commands[@]}"; do
    chmod +x bin/$cmd
done
