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
from scripting.prepare import get_frame
from scripting.config import unpack
from scripting.preprocess import preprocess
from scripting.execution import run


logger = logging.getLogger("Plot")
logging.basicConfig()


class Plot(Script):
    """
    Plot some data based on some config file
    """

    def __init__(self, *args):
        super(Plot, self).__init__(*args)
        self.io_scheme = "output_all"
        self.datasets = [os.path.dirname(os.path.abspath(f"{__file__}/.."))]
        self.optional["fit"] = False

    def execute(self):
        """
        Write plots
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
        reader = getattr(import_module(f"{module}.io"), names[0])
        build_plot = getattr(import_module(f"{module}.plot"), names[1])
        plot_data = getattr(import_module(f"{module}.plot"), names[2])
        if fit:
            calc_fit = getattr(import_module(
                f"{module}.process"), names[3])
            plot_fit = getattr(import_module(f"{module}.plot"), names[4])
        # Run
        outpath, outfn = None, None
        for i in range(len(infiles)):
            inpath, outpath = infiles[i], outfiles[i][0]
            if os.path.exists(outpath) and not overwrite:
                continue
            infn, outfn = os.path.basename(inpath), os.path.basename(outpath)
            logger.debug(f"Reading {infn}...")
            result = reader(inpath, **unpack(settings[names[0]], meta=meta))
            if pfunc != '':
                logger.debug(f"Applying {pfunc}...")
            result = preprocess(result, pfunc, meta)
            fig, ax = build_plot(**unpack(settings[names[1]], meta=meta))
            plot_data(*result, fig, ax,
                      **unpack(settings[names[2]], meta=meta))
            if fit:
                result = calc_fit(*result,
                                  **unpack(settings[names[3]], meta=meta))
                plot_fit(*result, fig, ax,
                         **unpack(settings[names[4]], meta=meta))
                ax.legend(loc=1)
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
    run(Plot, logger=logger)
