#!/bin/bash
#
# Make scripts into executables


commands=("setup-global" "setup-dataset" "setup-module" "update-dataset" "delete-dataset" "clean-out")

for cmd in "${commands[@]}"; do
    chmod +x $cmd
done
