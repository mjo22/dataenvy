#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file
"""

import os
import logging
import numpy as np
from scripting.config import load, unpack, shell_source
from scripting.prepare import get_files, get_settings, get_metadata
from scripting.execution import run


logger = logging.getLogger(__name__)
logging.basicConfig()


class Script(object):
    """
    An abstraction of a python script (very meta)
    """

    def __init__(self, configfile):
        # Read config
        self.config = unpack(load(configfile))
        # Source environment config if specified
        self.source()
        # Set variables that can be modified in subclass
        self.io_scheme = "output_all"
        self.datasets = os.environ['DATAPATHS'].split()
        self.required = ['inputext', 'outputext', 'inputdir', 'outputdir',
                         'module']
        self.optional = dict(minframe=-np.inf, maxframe=np.inf, nskip=0,
                             overwrite=True, glob='', outputlabel='',
                             preprocess='', ncpus=1)

    def prepare(self, **kwargs):
        """
        Prepare to execute script.
        """
        datasets, io_scheme, cfg = self.datasets, self.io_scheme, self.config
        self.metadata = get_metadata(datasets)
        self.set_config()
        self.files = get_files(cfg, datasets, io_scheme, **kwargs)
        self.settings = get_settings(cfg)

    def execute(self):
        """
        Overwrite to run script!
        """
        self.prepare()

    def source(self):
        """
        Source files specified in config
        """
        if "source" in self.config.keys():
            temp = self.config["source"]
            sources = temp if type(temp) is list else [temp]
            for source in sources:
                shell_source(source, verbose=0)

    def set_config(self):
        """
        Set default arguments in config
        """
        config, datasets = self.config, self.datasets
        # Setting optional config with metadata currently
        # only supporting for len(datasets) = 1
        meta = self.metadata[datasets[0]]
        required, optional = self.required, self.optional
        # Required arguments
        for k in required:
            if k not in config.keys():
                raise ValueError(f'{k} not in config')
        # Optional arguments
        for k1 in self.optional.keys():
            if k1 not in config.keys():
                config[k1] = optional[k1]
            else:
                try:
                    config[k1] = eval(config[k1])
                except (NameError, SyntaxError, TypeError) as err:
                    config[k1] = config[k1]
        return config


if __name__ == '__main__':
    run(Script, logger=logger)
