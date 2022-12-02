"""
Functions to preprocess data by keyword. These routines are a
table of preprocessing routines that act on the output of the
read_data.py routines before being handed off to analysis.

An example usage is the following: let's say read_data.py writes
a flow field to output. A routine can be calculated in this table
to compute its vorticity. Then, the same analysis can be performed
on the velocity and vorticity without writing extra data to disk.

To add routines to this file, use the skeleton

def myfunc(data, meta):
    # Process data
    result = process(data)  # You'll have to fill in how to process your data
    # Return result
    return result

Then, in your analysis config file MyConfig.toml, set

preprocess = 'myfunc'.
"""


def preprocess(data, funcnames, meta):
    def f(data, meta, funcs):
        if type(funcs) is str:
            return eval(funcs)(data, meta) if funcs != '' else data
        else:
            for func in funcnames:
                data = f(data, meta, func)
            return data
    if type(data) is tuple:
        return (f(data[0], meta, funcnames),)
    else:
        return f(data, meta, funcnames)
