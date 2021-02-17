#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file
"""

import os
import logging
import multiprocessing as mp
from matplotlib import pyplot as plt
from importlib import import_module
from scripting.Script import Script
from scripting.config import unpack
from scripting.preprocess import preprocess
from scripting.execution import run


logger = logging.getLogger("PlotMatch")
logging.basicConfig()


def dispatch(args):
    files, funcs, config, settings, metadata, datasets = args
    read, build_plot, plot_data = funcs[0], funcs[1], funcs[2]
    names = list(settings.keys())
    inpaths, outpaths, framenum = files
    outpath = outpaths[0] if type(outpaths) is list else outpaths
    logger.debug(f"Frame {framenum}")
    if not (os.path.exists(outpath) and not config['overwrite']):
        fig, ax = None, None
        for dataset in datasets:
            meta = metadata[dataset]
            if fig is None:
                fig, ax = build_plot(**unpack(settings[names[1]], meta=meta))
            inpath = inpaths[dataset]
            logger.debug(f"Reading {os.path.basename(inpath)}...")
            result = read(inpath, **unpack(settings[names[0]], meta=meta))
            logger.debug(f"Applying {config['preprocess']}...")
            result = preprocess(result, config['preprocess'], meta)
            plot = plot_data(*result, fig, ax,
                             **unpack(settings[names[2]], meta=meta))
            if config['fit']:
                calc_fit, plot_fit = funcs[3], funcs[4]
                result = calc_fit(*result,
                                  **unpack(settings[names[3]], meta=meta))
                plot_fit(*result, fig, ax, plot,
                         **unpack(settings[names[4]], meta=meta))
        logger.info(f"Writing {os.path.basename(outpath)}")
        ax.set_title(f"{config['title']} Frame {framenum}")
        plt.legend(loc=1, fontsize=8)
    fig.savefig(outpath)
    plt.close(fig)


class PlotMatch(Script):
    """
    Plot some data based on some config file, matching frame numbers
    in each dataset.
    """

    def __init__(self, *args):
        super(PlotMatch, self).__init__(*args)
        self.io_scheme = "match"
        self.optional["fit"] = False
        self.optional["title"] = ""
        self.required.append("outputlabel")
        del self.optional["outputlabel"]

    def execute(self):
        """
        Write plots
        """
        self.prepare(local=False)
        # Unpack fields
        datasets, config = self.datasets, self.config
        infiles, outfiles, frames = self.files
        metadata, settings = self.metadata, self.settings
        # Unpack config
        module, ncpus = config["module"], config["ncpus"]
        # Unpack functions
        names = list(settings.keys())
        read = getattr(import_module(f"{module}.io"), names[0])
        build_plot = getattr(import_module(f"{module}.plot"), names[1])
        plot_data = getattr(import_module(f"{module}.plot"), names[2])
        if config["fit"]:
            calc_fit = getattr(import_module(
                f"{module}.process"), names[3])
            plot_fit = getattr(import_module(f"{module}.plot"), names[4])
            funcs = (read, build_plot, plot_data, calc_fit, plot_fit)
        else:
            funcs = (read, build_plot, plot_data)
        # Args for dispatch
        a = (funcs, config, settings, metadata, datasets)
        # Run
        ncpus = os.cpu_count() if ncpus == -1 else ncpus
        nframes = len(frames)
        nchunks = nframes // ncpus
        for n in range(nchunks+1):
            nproc = ncpus if n < nchunks else nframes % ncpus
            args = []
            for m in range(nproc):
                idx = m+n*ncpus
                temp = {}
                for d in datasets:
                    temp[d] = infiles[d][idx]
                args.append(((temp, outfiles[idx], frames[idx]), *a))
            if nproc > 1:
                with mp.Pool(nproc) as pool:
                    pool.map(dispatch, args)
            elif nproc == 1:
                dispatch(args[0])
        if nframes > 0:
            delim = "_"
            outdir, outfn = os.path.split(outfiles[0][0])
            base = delim.join(os.path.basename(outfn).split(delim)[:-1])
            cmd = f"bash GenerateMovie.sh {outdir}/{base} ./PNG"
            os.system(cmd)


if __name__ == '__main__':
    run(PlotMatch, logger=logger)
