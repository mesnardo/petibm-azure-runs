"""Create the boundary of the snake cross-section.

Coordinates are saved in a Curve2D file in the `output` sub-folder.
"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Read the original coordinates of the section.
rootdir = pathlib.Path(__file__).absolute().parents[5]
datadir = rootdir / 'runs' / 'snake' / 'data'
filepath = datadir / 'snake2d.body'
with open(filepath, 'r') as infile:
    x, y = numpy.loadtxt(infile, skiprows=1, unpack=True)

# Apply rotation and regularize the geometry to desired resolution.
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-40.0)
x, y = petibmpy.regularize2d(x, y, ds=0.008)

# Write coordinates in file located in output directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
outdir = simudir / 'output'
filepath = outdir / 'snake2d40.curve'
with open(filepath, 'w') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y])
