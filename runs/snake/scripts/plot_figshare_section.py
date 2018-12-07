"""
Generate and save a figure of the snake cross-section.

The file with the coordinates was downloaded from Figshare.

References
----------

* Krishnan, Anush; J. Socha, John; P. Vlachos, Pavlos; Barba, Lorena A. (2013):
Body cross-section of the flying snake Chrysopelea paradisi. figshare. Fileset.
https://doi.org/10.6084/m9.figshare.705877.v1
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

# Plot the coordinates of the cross-section.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(4.0, 4.0))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid()
ax.plot(x, y)
ax.axis('equal')
fig.tight_layout()

# Save the figure as a PNG file.
fig_dir = root_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'snakeCrossSection.png'
fig.savefig(str(filepath), dpi=300)
