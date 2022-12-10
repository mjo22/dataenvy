"""
Routines for handling scripting input/output tasks
"""

import os
import glob
import numpy as np
from scripting.config import load


SCHEMES = ['match', 'output_all', 'output_one']


def get_metadata(datapaths):
    '''Read in metadata from each directory'''
    metadata = {}
    for datapath in datapaths:
        metadata[datapath] = load(os.path.join(datapath, "metadata.toml"))
    return metadata


def get_settings(config):
    """
    Load functions into sequential list
    """
    settings = {}
    for k1 in config.keys():
        if type(config[k1]) is dict:
            settings[k1] = config[k1]
    return settings


def get_files(config, datapaths, scheme, **kwargs):
    if scheme not in SCHEMES:
        raise NotImplementedError(f"Scheme {scheme} not supported")
    f = eval(scheme)
    return f(config, datapaths, **kwargs)


def match(config, datapaths, **kwargs):
    """
    Gather files based on matching frame-to-frame
    """
    inputfiles, frames = aggregate(config, datapaths, scheme='match', **kwargs)
    keys, N = list(frames.keys()), len(datapaths)
    for i in range(N):
        ki1 = keys[i]
        ki2 = keys[(i+1) % N]
        in1d = np.in1d(frames[ki1], frames[ki2], assume_unique=True)
        frames[ki1] = np.array(frames[ki1])[in1d]
        inputfiles[ki1] = np.array(inputfiles[ki1])[in1d]
    # Verify matching succeeded
    nframes = np.inf
    temp = None
    for k in keys:
        if len(frames[k]) <= nframes:
            nframes = len(frames[k])
            temp = k
    frames = frames[temp]
    # Create output files
    labels = config['outputlabel']
    labels = labels if type(labels) is list else [labels]
    outputdir, outext = config['outputdir'], config['outputext']
    outputfiles = []
    for i in range(nframes):
        frame = frames[i]
        fns = []
        for label in labels:
            fn = f"{label}{frame:05d}{outext}"
            fns.append(os.path.join(outputdir, fn))
        outputfiles.append(fns)
    return inputfiles, outputfiles, frames


def output_all(config, datapaths):
    """
    Output one file
    """
    return aggregate(config, datapaths, scheme='output_all')


def output_one(config, datapaths):
    """
    Output one file
    """
    return aggregate(config, datapaths, scheme='output_one')


def aggregate(config, datapaths, scheme='output_all', local=True):
    """
    Aggregate input files and set output files
    """
    if scheme not in SCHEMES:
        raise NotImplementedError(f"Scheme {scheme} not supported")
    ndatasets = len(datapaths)
    # Frame number params
    minframe, maxframe = config['minframe'], config['maxframe']
    nskip = config['nskip']
    # For file labeling
    label = config['outputlabel']
    # Get input files
    inputdir, outputdir = config['inputdir'], config['outputdir']
    inext, outext, glb = config['inputext'], config['outputext'], config['glob']
    glb = glb if glb != '' else f"*{config['inputext']}"
    inputfiles, outputfiles = {}, {}
    frames = {}
    for i in range(ndatasets):
        datapath = datapaths[i]
        # Frame selection
        fparams = []
        for param in [nskip, minframe, maxframe]:
            p = param[i] if type(param) is list else param
            fparams.append(p)
        # Loop preparation
        indir = os.path.join(datapath, inputdir)
        outdir = os.path.join(datapath, outputdir) if local else outputdir
        if not os.path.exists(outdir):
            print(f"Creating directory {outdir}")
            os.mkdir(outdir)
        globbed = sorted(glob.glob(f"{indir}/{glb}"))
        inputfiles[datapath], outputfiles[datapath] = [], []
        frames[datapath] = []
        done = False
        counter = fparams[0]
        for path in globbed:
            fn = os.path.basename(path)
            framenum = get_frame(fn, inext)
            if int(framenum) >= fparams[1] and int(framenum) <= fparams[2]:
                if counter == fparams[0]:
                    # Collect output filenames in list
                    basefn = f"{fn.replace(inext, outext)}"
                    if type(label) is list:
                        outpath = []
                        for lab in label:
                            outpath.append(os.path.join(
                                outdir, f"{lab}{basefn}"))
                    else:
                        outpath = [os.path.join(outdir, f"{label}{basefn}")]
                    # Add files based on output scheme
                    if scheme == 'output_one':
                        if not done:
                            for p in outpath:
                                temp = p.replace(f'_{framenum}', '')
                                outputfiles[datapath].append(temp)
                            done = True
                    elif scheme == 'output_all':
                        outputfiles[datapath].append(outpath)
                        frames[datapath].append(int(framenum))
                    elif scheme == 'match':
                        frames[datapath].append(int(framenum))
                    inputfiles[datapath].append(path)
                    counter = 0
                else:
                    counter += 1
    if scheme == 'output_all':
        return inputfiles, outputfiles, frames
    elif scheme == 'output_one':
        return inputfiles, outputfiles
    elif scheme == 'match':
        return inputfiles, frames


def get_frame(f, ext, delim='_'):
    """
    Gets frame number string of filename

    Assumes last section of string
    partitioned by delim is the frame
    number
    """
    basename = f.replace(ext, '')
    numstr = basename.split(delim)[-1]
    chars = [s for s in numstr.split() if s.isdigit()]
    tmp = ''
    framenum = tmp.join(chars)
    return framenum
