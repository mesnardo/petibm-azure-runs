"""
Generate the coordinates of the snake boundary.
"""

import sys
import pathlib
import numpy
from matplotlib import pyplot


root_dir = pathlib.Path(__file__).absolute().parents[6]

if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc

# Read the original coordinates of the section.
data_dir = root_dir / 'runs' / 'snake' / 'data'
filepath = data_dir / 'snake2d.body'
with open(filepath, 'r') as infile:
    x, y = numpy.loadtxt(infile, dtype=numpy.float64, skiprows=1, unpack=True)

# Rotate the section.
x, y = misc.rotate2d(x, y, center=(0.0, 0.0), angle=-25.0)
# Re-discretize the section.
x, y = misc.regularize2d(x, y, ds=0.008)

# Create coordinates for upstream and downstream sections.
x1, y1 = x.copy(), y.copy()
x2, y2 = x.copy(), y.copy()

# Displace the downstream section.
chord = 1.0
gap, stagger = 5 * chord, -chord
x2 += gap
y2 += stagger

show_figure = False
if show_figure:
    pyplot.rc('font', family='serif', size=16)
    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid()
    ax.plot(x1, y1, label='Upstream', marker='x')
    ax.plot(x2, y2, label='Downstream', marker='x')
    ax.legend()
    ax.axis('scaled', adjust='box')
    pyplot.show()

# Extrude the sections along the z direction.
x1, y1, z1 = misc.extrude2d(x1, y1, ds=0.08, limits=(0.0, 3.2))
x2, y2, z2 = misc.extrude2d(x2, y2, ds=0.08, limits=(0.0, 3.2))

# Write new coordinates in files located in simulation directory.
simu_dir = pathlib.Path(__file__).absolute().parents[1]
bodies_dir = simu_dir / 'bodies'
bodies_dir.mkdir(parents=True, exist_ok=True)
filepath = bodies_dir / 'snake3d25_upstream.body'
with open(filepath, 'w') as outfile:
    outfile.write(f'{x1.size}\n')
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x1, y1, z1])
filepath = bodies_dir / 'snake3d25_downstream.body'
with open(filepath, 'w') as outfile:
    outfile.write(f'{x2.size}\n')
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x2, y2, z2])
