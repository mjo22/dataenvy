#!/usr/bin/env python

"""
Script to write metadata to a directory for
other scripts to read in
"""

import os
from scripting.config import dump, unpack


DATAPATH = os.environ["PWD"]
SOURCE_CFG = os.path.abspath("PLACEHOLDER/XXX")


def read_config(fn):
    d = {}
    return d


def main():
    """
    Write metadata to metadata.toml
    """
    label = os.path.basename(DATAPATH).replace("_", " ")
    metadata = {"label": label}
    metadata = {**metadata, **read_config(SOURCE_CFG)}
    keys = []
    for k in keys:
        value = input(f"Enter a value for {k}: ")
        metadata[k] = value
    outputpath = "metadata.toml"
    dump(unpack(metadata), outputpath)


if __name__ == "__main__":
    main()
