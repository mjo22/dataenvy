#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file and plots the results
"""

import os
import logging
import multiprocessing as mp
from matplotlib import pyplot as plt
from importlib import import_module
from scripting.Script import Script
from scripting.prepare import get_frame
from scripting.config import unpack
from scripting.execution import run
from processing.preprocess import preprocess


logger = logging.getLogger("Plot")
logging.basicConfig()


def dispatch(args):
    files, funcs, config, settings, meta = args
    read, build_plot, plot_data = funcs[0], funcs[1], funcs[2]
    names = list(settings.keys())
    inpath, outpaths = files
    outpath = outpaths[0] if type(outpaths) is list else outpaths
    infn, outfn = os.path.basename(inpath), os.path.basename(outpath)
    if not (os.path.exists(outpath) and not config['overwrite']):
        logger.debug(f"Reading {infn}...")
        result = read(inpath, **unpack(settings[names[0]], meta=meta))
        logger.debug(f"Applying {config['preprocess']}...")
        result = preprocess(result, config['preprocess'], meta)
        fig, ax = build_plot(**unpack(settings[names[1]], meta=meta))
        plot = plot_data(*result, fig=fig, ax=ax,
                         **unpack(settings[names[2]], meta=meta))
        logger.debug(f"Plotting {plot_data.__name__}...")
        if config['fit']:
            calc_fit, plot_fit = funcs[3], funcs[4]
            logger.debug(f"Fitting {calc_fit.__name__}...")
            result = calc_fit(*result,
                              **unpack(settings[names[3]], meta=meta))
            plot_fit(*result, fig, ax, plot,
                     **unpack(settings[names[4]], meta=meta))
            ax.legend(loc=1)
        logger.info(f"Writing {outfn}")
        framenum = get_frame(outfn, config['outputext'])
        if config["title"] is not None:
            title = config["title"]
        else:
            title = f"{meta['label']} frame {framenum}"
        ax.set_title(f"{ax.get_title()} {title}")
        fig.savefig(outpath)
        plt.close(fig)
    else:
        logger.debug(f"Skipping {outfn} (already written)")


class Plot(Script):
    """
    Plot some data based on some config file
    """

    def __init__(self, *args):
        super(Plot, self).__init__(*args)
        self.io_scheme = "output_all"
        self.optional["fit"] = False
        self.optional["title"] = None

    def execute(self):
        """
        Write plots
        """
        self.prepare()
        # Unpack fields
        d, config = self.datasets[0], self.config
        infiles, outfiles = self.files[0][d], self.files[1][d]
        meta, settings = self.metadata[d], self.settings
        # Unpack config
        module, ncpus = config["module"], config["ncpus"]
        # Unpack functions
        names = list(settings.keys())
        read = getattr(import_module(f"{module}.io"), names[0])
        build_plot = getattr(import_module(f"{module}.plot"), names[1])
        plot_data = getattr(import_module(f"{module}.plot"), names[2])
        if config['fit']:
            calc_fit = getattr(import_module(f"{module}.process"), names[3])
            plot_fit = getattr(import_module(f"{module}.plot"), names[4])
            funcs = (read, build_plot, plot_data, calc_fit, plot_fit)
        else:
            funcs = (read, build_plot, plot_data)
        # Args for dispatch
        a = (funcs, config, settings, meta)
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
            # Generate movie
            if nfiles > 1:
                delim = "_"
                outdir, outfn = os.path.split(outfiles[0][0])
                base = delim.join(os.path.basename(outfn).split(delim)[:-1])
                cmd = f"bash {d}/{module}/GenerateMovie.sh {outdir}/{base} {d}/PNG"
                os.system(cmd)
        else:
            dataset = os.path.basename(d)
            inputdir = os.path.join(dataset, config['inputdir'])
            inputpath = os.path.join(inputdir, config['glob'])
            logger.debug(f"No input files found for {inputpath} between frames {config['minframe']}-{config['maxframe']}.")


if __name__ == '__main__':
    run(Plot, logger=logger)
