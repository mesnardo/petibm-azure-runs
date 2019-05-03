"""Generate the coordinates of the snake boundary."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[5]

# Read the original coordinates of the section.
datadir = rootdir / 'runs' / 'snake' / 'data'
filepath = datadir / 'snake2d.body'
with open(filepath, 'r') as infile:
    x, y = numpy.loadtxt(infile, skiprows=1, unpack=True)

# Apply rotation and regularize the geometry to desired resolution.
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-20.0)
x, y = petibmpy.regularize2d(x, y, ds=0.008)
# Extrude the section along the z direction.
x, y, z = petibmpy.extrude2d(x, y, ds=0.08, limits=(0.0, 3.2))

# Write new coordinates in file located in simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'snake3d20.body'
with open(filepath, 'w') as outfile:
    outfile.write(f'{x.size}\n')
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y, z])
