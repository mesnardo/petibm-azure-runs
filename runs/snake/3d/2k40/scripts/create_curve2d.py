"""
Generate the coordinates of the snake boundary.
"""

import sys
import pathlib
import numpy
from matplotlib import pyplot


root_dir = pathlib.Path(__file__).absolute().parents[5]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc

# Read the original coordinates of the section.
data_dir = root_dir / 'runs' / 'snake' / 'data'
filepath = data_dir / 'snake2d.body'
with open(filepath, 'r') as infile:
    x, y = numpy.loadtxt(infile, dtype=numpy.float64, skiprows=1, unpack=True)

# Apply rotation and regularize the geometry to desired resolution.
x, y = misc.rotate2d(x, y, center=(0.0, 0.0), angle=-40.0)
x, y = misc.regularize2d(x, y, ds=0.008)

# Write coordinates in file located in output directory.
simu_dir = pathlib.Path(__file__).absolute().parents[1]
out_dir = simu_dir / 'output'
filepath = out_dir / 'snake2d40.curve'
with open(filepath, 'w') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y])
