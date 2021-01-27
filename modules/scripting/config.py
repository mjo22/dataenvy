"""
Convenience methods for handling script and data configuration
"""

import numpy as np
import toml


def load(fn, **kwargs):
    return toml.load(fn, **kwargs)


def unpack(d, meta=None):
    """
    Loads dict read some toml file and evaluates its contents.
    Meta variable and numpy import allow for
    versatile configuration.

    Parameters
    ----------
    d : dict

    Keywords
    --------
    meta : anything
        A global variable to refer to in config files

    Returns
    -------
    d : dict
        Dictionary represention of section.
    """
    for k in d.keys():
        if type(d[k]) is str:
            try:
                d[k] = eval(d[k])
            except (NameError, SyntaxError, TypeError) as err:
                pass
        elif type(d[k]) is dict:
            d[k] = unpack(d[k], meta=meta)
        else:
            pass
    return d


def dump(d, fn, **kwargs):
    """
    Dumps dictionary into .toml file
    """
    with open(fn, 'w') as f:
        parsed = toml.dump(d, f, **kwargs)
    return parsed
