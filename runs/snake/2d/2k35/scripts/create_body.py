"""Create the boundary of the snake cross-section.

The boundary coordinates are saved to file.
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
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-35.0)
x, y = petibmpy.regularize2d(x, y, ds=0.004)

# Write new coordinates in file located in simulation directory.
simu_dir = pathlib.Path(__file__).absolute().parents[1]
filepath = simu_dir / 'snake2d35.body'
petibmpy.write_body(filepath)
