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
from utilities.fits import read_hdul


logger = logging.getLogger("WriteData")
logging.basicConfig()


class WriteData(Script):
    """
    Write some data based on some config file
    """

    def __init__(self, *args):
        super(WriteData, self).__init__(*args)
        self.io_scheme = "output_all"
        self.datasets = [os.path.dirname(os.path.abspath(f"{__file__}/.."))]

    def execute(self):
        """
        Write data
        """
        self.prepare()
        # Unpack
        d, config = self.datasets[0], self.config
        overwrite, pfunc = self.config["overwrite"], self.config["preprocess"]
        infiles, outfiles = self.files[0][d], self.files[1][d]
        meta, settings = self.metadata[d], self.settings
        # Get functions
        module = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        # Unpack functions
        names = list(settings.keys())
        calculate = getattr(import_module(f"{module}.process"), names[0])
        write = getattr(import_module(f"{module}.io"), names[1])
        for i in range(len(infiles)):
            inpath, outpath = infiles[i], outfiles[i][0]
            if os.path.exists(outpath) and not overwrite:
                continue
            infn, outfn = os.path.basename(inpath), os.path.basename(outpath)
            logger.debug(f"Reading {infn}...")
            data = read_hdul(inpath)[0]
            if pfunc != '':
                logger.debug(f"Applying {pfunc}...")
            data = preprocess(data, pfunc, meta)
            logger.debug("Calculating...")
            result = calculate(data, **unpack(settings[names[0]], meta=meta))
            logger.info(f"Writing {outfn}")
            write(*result, outfiles[i], overwrite=overwrite,
                  **unpack(settings[names[1]], meta=meta))


if __name__ == '__main__':
    run(WriteData, logger=logger)
