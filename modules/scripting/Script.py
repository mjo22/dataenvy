#!/usr/bin/env python

"""
Python script that executes a set of functions specified in a
config file
"""

import os
import logging
import numpy as np
from scripting.config import load, unpack, shell_source
from scripting.read import get_files, get_settings, get_metadata
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
        if "configenvy" in self.config.keys():
            if "DATAENVY" not in os.environ.keys():
                raise ValueError("bash variable DATAENVY not set.")
            dataenvy, args = os.environ['DATAENVY'], self.config['configenvy']
            shell_source(f"{dataenvy}/configenvy {args}", verbose=1)
        # Set variables that can be modified in subclass
        self.io_scheme = "output_all"
        self.datasets = os.environ['DATAPATHS'].split()
        self.required = ['inputext', 'outputext', 'inputdir', 'outputdir']
        self.optional = {'minframe': -np.inf, 'maxframe': np.inf, 'nskip': 0,
                         'overwrite': True, 'glob': '',
                         'outputlabel': '', 'preprocess': ''}

    def prepare(self):
        """
        Prepare to execute script.
        """
        datasets, io_scheme, cfg = self.datasets, self.io_scheme, self.config
        self.metadata = get_metadata(datasets)
        self.set_config()
        self.files = get_files(cfg, datasets, io_scheme)
        self.settings = get_settings(cfg)

    def execute(self):
        """
        Overwrite to run script!
        """
        self.prepare()

    def set_config(self):
        """
        Set default arguments in config
        """
        config = self.config
        required, optional = self.required, self.optional
        # Required arguments
        for k in required:
            if k not in config.keys():
                raise ValueError(f'{k} not in config')
        # Expand to absolute paths and create directories
        for path in self.datasets:
            config["inputdir"] = os.path.join(path, config["inputdir"])
            config["outputdir"] = os.path.join(path, config["outputdir"])
            if not os.path.exists(config["outputdir"]):
                print(f"Creating directory {config['outputdir']}")
                os.mkdir(config["outputdir"])
        # Optional arguments
        for k1 in self.optional.keys():
            if k1 not in config.keys():
                config[k1] = optional[k1]
        return config


if __name__ == '__main__':
    run(Script, logger=logger)
