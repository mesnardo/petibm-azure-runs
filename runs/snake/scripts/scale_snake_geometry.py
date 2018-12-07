"""
Read the coordinates from the file downloaded from Figshare,
scale the geometry to have a unitary chord length,
and write the scaled coordinates into a file.
"""

import pathlib
import numpy
from matplotlib import pyplot


root_dir = pathlib.Path(__file__).absolute().parents[1]
data_dir = root_dir / 'data'

# Read the cross-section coordinates from file.
filepath = data_dir / 'SnakeCrossSection.txt'
with open(filepath, 'r') as infile:
    x, y = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)

# Scale the geometry to have a chord length of 1.
chord = x.max() - x.min()
x /= chord
y /= chord
x -= (x.max() + x.min()) / 2
y -= (y.max() + y.min()) / 2

# Write the coordinates into a file.
filepath = data_dir / 'snake2d.body'
with open(filepath, 'w') as outfile:
    outfile.write(f'{x.size}\n')
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y])
