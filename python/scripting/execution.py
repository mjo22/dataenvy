"""
Routines for executing scripts based on a number of execution schemes
"""

import argparse
import os
import logging


def run(Script, logger=None):
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str,
                        help="Configuration file")
    parser.add_argument("-l", "--log", type=str,
                        help="Set level of logger")
    # Unpack argument parser
    args = parser.parse_args()
    configfile = os.path.abspath(os.path.expanduser(args.config))
    loglevel = args.log if args.log is not None else "INFO"
    # Set level of logging
    if logger is not None:
        logger.setLevel(getattr(logging, loglevel.upper()))
    # Execute
    a = Script(configfile)
    a.execute()
