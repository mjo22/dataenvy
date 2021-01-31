#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file
"""

import os
import logging
from matplotlib import pyplot as plt
from importlib import import_module
from scripting.Script import Script
from scripting.config import unpack
from scripting.preprocess import preprocess
from scripting.execution import run


logger = logging.getLogger("PlotMatch")
logging.basicConfig()


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
        # Unpack settings
        datasets, config = self.datasets, self.config
        overwrite, pfunc = config["overwrite"], config["preprocess"]
        infiles, outfiles, frames = self.files
        metadata, settings = self.metadata, self.settings
        fit = config["fit"]
        # Get module
        module = config["module"]
        # Unpack functions
        names = list(settings.keys())
        reader = getattr(import_module(f"{module}.io"), names[0])
        build_plot = getattr(import_module(f"{module}.plot"), names[1])
        plot_data = getattr(import_module(f"{module}.plot"), names[2])
        if fit:
            calc_fit = getattr(import_module(
                f"{module}.process"), names[3])
            plot_fit = getattr(import_module(f"{module}.plot"), names[4])
        # Run
        outpath = None
        nframes = len(frames)
        for i in range(nframes):
            framenum = frames[i]
            logger.debug(f"Frame {framenum}/{nframes}")
            outpath = outfiles[i][0]
            outfn = os.path.basename(outpath)
            if os.path.exists(outpath) and not overwrite:
                continue
            fig, ax = None, None
            for dataset in datasets:
                meta = metadata[dataset]
                if fig is None:
                    fig, ax = build_plot(
                        **unpack(settings[names[1]], meta=meta))
                inpath = infiles[dataset][i]
                logger.debug(f"Reading {os.path.basename(inpath)}...")
                result = reader(inpath,
                                **unpack(settings[names[0]], meta=meta))
                if pfunc != '':
                    logger.debug(f"Applying {pfunc}...")
                result = preprocess(result, pfunc, meta)
                plot_data(*result, fig, ax,
                          **unpack(settings[names[2]], meta=meta))
                if fit:
                    result = calc_fit(*result,
                                      **unpack(settings[names[3]], meta=meta))
                    plot_fit(*result, fig, ax,
                             **unpack(settings[names[4]], meta=meta))
            logger.info(f"Writing {os.path.basename(outpath)}")
            ax.set_title(f"{config['title']} Frame {framenum}")
            plt.legend(loc=1)
            fig.savefig(outpath)
            plt.close(fig)
        if outpath is None:
            raise IOError("No input files found")
        # Generate movie
        delim = "_"
        indir = os.path.dirname(outpath)
        base = delim.join(os.path.basename(outfn).split(delim)[:-1])
        os.system(f"bash GenerateMovie.sh {indir}/{base} ./PNG")


if __name__ == '__main__':
    run(PlotMatch, logger=logger)
