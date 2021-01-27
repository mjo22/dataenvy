"""
Functions to preprocess data by keyword
"""

import numpy as np


def preprocess(data, funcname):
    def f(data):
        return eval(funcname)(data) if funcname != '' else data
    if type(data) is tuple:
        return (f(data[0]),)
    else:
        return f(data)


def ravel(data):
    return data.ravel()
