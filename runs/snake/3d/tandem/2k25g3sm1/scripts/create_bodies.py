"""Create the boundary of the snake cross-sections.

The two boundaries are saved in the sub-folder `bodies`.
"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Read the original coordinates of the section.
rootdir = pathlib.Path(__file__).absolute().parents[6]
datadir = rootdir / 'runs' / 'snake' / 'data'
filepath = datadir / 'snake2d.body'
x, y = petibmpy.read_body(filepath, skiprows=1)

# Rotate the section.
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-25.0)
# Re-discretize the section.
x, y = petibmpy.regularize2d(x, y, ds=0.008)

# Duplicate the section (create a new for the downstream section).
xd, yd = x.copy(), y.copy()

# Displace the downstream section.
chord = 1.0  # cross-section chord length
gap, stagger = 3 * chord, - chord
xd += gap
yd += stagger

# Extrude the sections along the z direction.
x, y, z = petibmpy.extrude2d(x, y, ds=0.08, limits=(0.0, 3.2))
xd, yd, zd = petibmpy.extrude2d(xd, yd, ds=0.08, limits=(0.0, 3.2))

# Write new coordinates in files located in simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
outdir = simudir / 'bodies'
outdir.mkdir(parents=True, exist_ok=True)
filepath = outdir / 'snake3d25_upstream.body'
petibmpy.write_body(filepath, x, y, z)
filepath = outdir / 'snake3d25_downstream.body'
petibmpy.write_body(filepath, xd, yd, zd)
