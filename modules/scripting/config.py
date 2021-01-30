"""
Convenience methods for handling script and data configuration
"""

import numpy as np
import toml
import os
import subprocess


def load(fn, **kwargs):
    return toml.load(fn, **kwargs)


def unpack(settings, meta=None):
    """
    Loads dict read some toml file and evaluates its contents.
    Meta variable and numpy import allow for
    versatile configuration.

    Parameters
    ----------
    settings : dict

    Keywords
    --------
    meta : anything
        A global variable to refer to in config files

    Returns
    -------
    d : dict
        Dictionary represention of section.
    """
    d = {}
    for k in settings.keys():
        if type(settings[k]) is str:
            try:
                d[k] = eval(settings[k])
            except (NameError, SyntaxError, TypeError) as err:
                d[k] = settings[k]
        elif type(settings[k]) is dict:
            d[k] = unpack(settings[k], meta=meta)
        else:
            d[k] = settings[k]
    return d


def dump(d, fn, **kwargs):
    """
    Dumps dictionary into .toml file
    """
    with open(fn, 'w') as f:
        parsed = toml.dump(d, f, **kwargs)
    return parsed


def shell_source(script, verbose=0):
    """
    Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it.

    Parameters
    ----------
    script : str
        Script and its bash arguments to execute.
    Keywords
    --------
    verbose : int
        Check what was modified in env to make sure behavior
        is expected. Set as 0 --> 2 for increasing levels of
        verbosity.

    WARNING: Using the shell=True option in Popen comes with
             security risks. Read about it here:
             https://docs.python.org/3/library/subprocess.html#security-considerations
    NOTE: This will not work if the source script attempts to unset
          variables.

    Modified from user Federico on the following thread:
    https://stackoverflow.com/questions/7040592/calling-the-source-command-from-subprocess-popen
    """
    env = os.environ
    pipe = subprocess.Popen(f". {script} && env -0",
                            stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0].decode('utf-8')
    # Fix for index out for range in 'env[line[0]] = line[1]'
    output = output[:-1]

    newenv = {}
    # Split using null char
    for line in output.split('\x00'):
        line = line.split('=', 1)
        newenv[line[0]] = line[1]

    # Don't modify variables that are modified by nature of
    # calling this funciton
    expected = ["SHLVL", "_"]
    for k in expected:
        if verbose > 1:
            print(f"Fixing: {k}={newenv[k]} -> {env[k]}")
        newenv[k] = env[k]

    # Reset variables that were present in initial python env
    for k in env.keys():
        if k not in newenv:
            # Assuming things are not intentionally unset by python
            if verbose > 1:
                print(f"Adding: {k}={env[k]}")
            newenv[k] = env[k]

    # Check what was modified
    if verbose > 0:
        for k in newenv.keys():
            if k not in env.keys():
                print(f"Set: {k}={newenv[k]}")
            else:
                if newenv[k] != env[k]:
                    print(f"Modified: {k}={env[k]} -> {newenv[k]}")

    os.environ.update(newenv)
