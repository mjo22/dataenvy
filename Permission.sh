#!/bin/bash
#
# Make scripts into executables


commands=("setup-global" "setup-module" "setup-dataset" "sync-dataset" "write-dataset" "delete-dataset" "clean-out")

for cmd in "${commands[@]}"; do
    chmod +x $cmd
done
