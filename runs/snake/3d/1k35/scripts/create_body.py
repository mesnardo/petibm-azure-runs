"""Generate the coordinates of the snake boundary."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[5]

# Read the original coordinates of the section.
datadir = rootdir / 'runs' / 'snake' / 'data'
filepath = datadir / 'snake2d.body'
x, y = petibmpy.read_body(filepath, skiprows=1)

# Apply rotation and regularize the geometry to desired resolution.
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-35.0)
x, y = petibmpy.regularize2d(x, y, ds=0.008)
# Extrude the section along the z direction.
x, y, z = petibmpy.extrude2d(x, y, ds=0.08, limits=(0.0, 3.2))

# Write new coordinates in file located in simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'snake3d35.body'
petibmpy.write_body(filepath, x, y, z)
