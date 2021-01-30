#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file
"""

import os
import logging
from importlib import import_module
from scripting.Script import Script
from scripting.config import unpack
from scripting.execution import run
from scripting.preprocess import preprocess

logger = logging.getLogger("Write")
logging.basicConfig()


class Write(Script):
    """
    Write some data based on some config file
    """

    def __init__(self, *args):
        super(Write, self).__init__(*args)
        self.io_scheme = "output_all"

    def execute(self):
        """
        Write data
        """
        self.prepare()
        # Unpack
        d, config = self.datasets[0], self.config
        overwrite, func = config["overwrite"], config["preprocess"]
        infiles, outfiles = self.files[0][d], self.files[1][d]
        meta, settings = self.metadata[d], self.settings
        # Get functions
        module = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        # Unpack functions
        names = list(settings.keys())
        read = getattr(import_module("scripting.read_data"), names[0])
        calculate = getattr(import_module(f"{module}.process"), names[1])
        write = getattr(import_module(f"{module}.io"), names[2])
        for i in range(len(infiles)):
            inpath, outpath = infiles[i], outfiles[i][0]
            if os.path.exists(outpath) and not overwrite:
                continue
            infn, outfn = os.path.basename(inpath), os.path.basename(outpath)
            logger.debug(f"Reading {infn}...")
            data = read(inpath, **unpack(settings[names[0]], meta=meta))
            if func != '':
                logger.debug(f"Applying {func}...")
            data = preprocess(data, func, meta)
            logger.debug("Calculating...")
            result = calculate(data, **unpack(settings[names[1]], meta=meta))
            logger.info(f"Writing {outfn}")
            write(*result, outfiles[i], overwrite=overwrite,
                  **unpack(settings[names[2]], meta=meta))


if __name__ == '__main__':
    run(Write, logger=logger)
