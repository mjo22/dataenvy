#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file
"""

import os
import logging
import multiprocessing as mp
from importlib import import_module
from scripting.Script import Script
from scripting.config import unpack
from scripting.execution import run
from processing.preprocess import preprocess

logger = logging.getLogger("Write")
logging.basicConfig()


def dispatch(args):
    files, funcs, config, settings, meta = args
    read, calculate, write = funcs
    r, c, w = list(settings.keys())
    inpath, outpaths = files
    outpath = outpaths[0] if type(outpaths) is list else outpaths
    infn, outfn = os.path.basename(inpath), os.path.basename(outpath)
    if not (os.path.exists(outpath) and not config['overwrite']):
        logger.debug(f"Reading {infn}...")
        data = read(inpath, **unpack(settings[r], meta=meta))
        logger.debug(f"Applying {config['preprocess']}...")
        data = preprocess(data, config['preprocess'], meta)
        logger.debug(f"Calculating {calculate.__name__}...")
        result = calculate(data, **unpack(settings[c], meta=meta))
        logger.info(f"Writing {outfn}")
        write(outpaths, *result, overwrite=config['overwrite'],
              **unpack(settings[w], meta=meta))
   else:
        logger.debug(f"Skipping {outfn} (already written)")


class Write(Script):
    """
    Write some data based on some config file
    """

    def __init__(self, *args):
        super(Write, self).__init__(*args)
        self.io_scheme = "output_all"

    def execute(self):
        '''Write data'''
        self.prepare()
        # Unpack fields
        d, config = self.datasets[0], self.config
        infiles, outfiles = self.files[0][d], self.files[1][d]
        meta, settings = self.metadata[d], self.settings
        # Unpack config
        module, ncpus = config["module"], config["ncpus"]
        # Unpack functions
        r, c, w = list(settings.keys())
        read = getattr(import_module("processing.read_data"), r)
        calculate = getattr(import_module(f"{module}.process"), c)
        write = getattr(import_module(f"{module}.io"), w)
        # Args for dispatch function
        a = ((read, calculate, write), config, settings, meta)
        # Run
        ncpus = os.cpu_count() if ncpus == -1 else ncpus
        nfiles = len(infiles)
        if nfiles > 0:
            nchunks = nfiles // ncpus
            for n in range(nchunks+1):
                nproc = ncpus if n < nchunks else nfiles % ncpus
                args = []
                for m in range(nproc):
                    idx = m+n*ncpus
                    args.append(((infiles[idx], outfiles[idx]), *a))
                if nproc > 1:
                    with mp.Pool(nproc) as pool:
                        pool.map(dispatch, args)
                elif nproc == 1:
                    dispatch(args[0])
        else:
            dataset = os.path.basename(d)
            inputdir = os.path.join(dataset, config['inputdir'])
            inputpath = os.path.join(inputdir, config['glob'])
            logger.debug(f"No input files found for {inputpath} between frames {config['minframe']}-{config['maxframe']}.")


if __name__ == '__main__':
    run(Write, logger=logger)
