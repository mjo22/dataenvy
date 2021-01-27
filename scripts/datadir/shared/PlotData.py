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
from scripting.read import get_frame
from scripting.config import unpack
from scripting.preprocess import preprocess
from scripting.execution import run


logger = logging.getLogger("PlotData")
logging.basicConfig()


class PlotData(Script):
    """
    Plot a statistic based on some config file
    """

    def __init__(self, *args):
        datapath = os.path.dirname(os.path.abspath(f"{__file__}/.."))
        super(PlotData, self).__init__(*args,
                                       datapaths=[datapath],
                                       io_scheme="output_all")
        self.optional["fit"] = False
        self.required.extend(["reader"])

    def execute(self):
        """
        Write powerspectrum plots
        """
        self.prepare()
        # Get module
        module = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        # Unpack settings
        d, config = self.datasets[0], self.config
        overwrite, pfunc = config["overwrite"], config["preprocess"]
        infiles, outfiles = self.files[0][d], self.files[1][d]
        meta, settings = self.metadata[d], self.settings
        fit = config["fit"]
        # Unpack functions
        names = list(settings.keys())
        build_plot = getattr(import_module(f"{module}.plot"), names[0])
        plot_stat = getattr(import_module(f"{module}.plot"), names[1])
        if fit:
            calc_fit = getattr(import_module(
                f"{module}.process"), names[2])
            plot_fit = getattr(import_module(f"{module}.plot"), names[3])
        # Get data reader
        reader = getattr(import_module(f"{module}.io"), config["reader"])
        # Run
        for i in range(len(infiles)):
            inpath, outpath = infiles[i], outfiles[i][0]
            if os.path.exists(outpath) and not overwrite:
                continue
            infn, outfn = os.path.basename(inpath), os.path.basename(outpath)
            logger.debug(f"Reading {infn}...")
            result = reader(inpath)
            if pfunc != '':
                logger.debug(f"Applying {pfunc}...")
            result = preprocess(result, pfunc)
            fig, ax = build_plot(**unpack(settings[names[0]], meta=meta))
            plot_stat(*result, fig, ax,
                      **unpack(settings[names[1]], meta=meta))
            if fit:
                result = calc_fit(*result,
                                  **unpack(settings[names[2]], meta=meta))
                plot_fit(*result, fig, ax,
                         **unpack(settings[names[3]], meta=meta))
            logger.info(f"Writing {outfn}")
            framenum = get_frame(outfn, config['outputext'])
            ax.set_title(f"{meta['label']} Frame {framenum}")
            fig.savefig(outpath)
            plt.close(fig)
        # Generate movie
        delim = "_"
        indir = os.path.dirname(outpath)
        base = delim.join(os.path.basename(outfn).split(delim)[:-1])
        os.system(f"bash {d}/{module}/GenerateMovie.sh {indir}/{base} {d}/PNG")


if __name__ == '__main__':
    run(PlotData, logger=logger)
