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
x, y = misc.rotate2d(x, y, center=(0.0, 0.0), angle=-20.0)
x, y = misc.regularize2d(x, y, ds=0.008)
# Extrude the section along the z direction.
x, y, z = misc.extrude2d(x, y, ds=0.08, limits=(0.0, 3.2))

# Write new coordinates in file located in simulation directory.
simu_dir = pathlib.Path(__file__).absolute().parents[1]
filepath = simu_dir / 'snake3d20.body'
with open(filepath, 'w') as outfile:
    outfile.write(f'{x.size}\n')
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y, z])
