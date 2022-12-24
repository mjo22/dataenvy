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
from processing.preprocess import preprocess

logger = logging.getLogger("Average")
logging.basicConfig()


class Average(Script):
    """
    Aggregate and contract some data based on a config file
    """

    def __init__(self, *args):
        super(Average, self).__init__(*args)
        self.io_scheme = "output_one"

    def execute(self):
        '''Write data'''
        self.prepare()
        # Unpack fields
        d, config = self.datasets[0], self.config
        inpaths, outpaths = self.files[0][d], self.files[1][d]
        meta, settings = self.metadata[d], self.settings
        # Unpack config
        module = config["module"]
        # Unpack functions
        r, c, w = list(settings.keys())
        read = getattr(import_module(f"{module}.io"), r)
        calculate = getattr(import_module(f"{module}.process"), c)
        write = getattr(import_module(f"{module}.io"), w)
        # Run
        nfiles = len(inpaths)
        if nfiles > 0:
            outpath = outpaths[0] if type(outpaths) is list else outpaths
            outfn = os.path.basename(outpath)
            if not (os.path.exists(outpath) and not config['overwrite']):
                data = []
                for inpath in inpaths:
                    infn = os.path.basename(inpath)
                    logger.debug(f"Reading {infn}...")
                    temp = read(inpath, **unpack(settings[r], meta=meta))
                    logger.debug(f"Applying {config['preprocess']}...")
                    temp = preprocess(temp, config['preprocess'], meta)
                    data.append(temp)
                logger.debug(f"Calculating {calculate.__name__}...")
                result = calculate(data, **unpack(settings[c], meta=meta))
                logger.info(f"Writing {outfn}")
                write(outpaths, *result, overwrite=config['overwrite'],
                      **unpack(settings[w], meta=meta))
            else:
                logger.debug(f"Skipping {outfn} (already written)")
        else:
            dataset = os.path.basename(d)
            inputdir = os.path.join(dataset, config['inputdir'])
            inputpath = os.path.join(inputdir, config['glob'])
            logger.debug(f"No input files found for {inputpath} between frames {config['minframe']}-{config['maxframe']}.")


if __name__ == '__main__':
    run(Average, logger=logger)
