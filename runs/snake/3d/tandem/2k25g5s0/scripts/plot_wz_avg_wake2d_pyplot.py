"""Plot the spanwise-averaged z-vorticity at saved time steps."""

from matplotlib import pyplot
import numpy
import pathlib
import yaml

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output' / 'postprocessing' / 'wz_avg'

# Read the gridline coordinates from file.
filepath = datadir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, 'wz-avg')

# Read the coordinates of the bodies from files.
filepath = simudir / 'bodies' / 'snake3d25_upstream.body'
xb1, yb1, zb1 = petibmpy.read_body(filepath, skiprows=1)
# Keep only a 2D cross-section.
n = len(numpy.where(zb1 == zb1[0])[0])
xb1, yb1 = xb1[:n], yb1[:n]
filepath = simudir / 'bodies' / 'snake3d25_downstream.body'
xb2, yb2, zb2 = petibmpy.read_body(filepath, skiprows=1)
# Keep only a 2D cross-section.
n = len(numpy.where(zb2 == zb2[0])[0])
xb2, yb2 = xb2[:n], yb2[:n]

# Get temporal parameters.
filepath = simudir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)['parameters']
dt, nstart, nt, nsave = (config[k] for k in ['dt', 'startStep', 'nt', 'nsave'])
timesteps = list(range(nstart, nstart + nt + 1, nsave))

# Create the directory to save the figures.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)

# Initialize the figure and axis.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(12.0, 4.0))
ax.set_xlabel('x')
ax.set_ylabel('y')
text = ax.text(-0.5, 0.8, '',
               bbox=dict(facecolor='white', edgecolor='white'), zorder=5)
ax.fill(xb1, yb1, color='black', zorder=10)
ax.fill(xb2, yb2, color='black', zorder=10)
levels = numpy.linspace(-5.0, 5.0, num=50)
cont = None
ax.axis('scaled', adjustable='box')
ax.set_xlim(-0.6, 8.5)
ax.set_ylim(-1.0, 1.0)
fig.tight_layout()

# Generate the filled contour at each saved time step.
for timestep in timesteps:
    print('[time step {:0>7}] Generating the figure...'.format(timestep))
    filepath = datadir / '{:0>7}.h5'.format(timestep)
    wz = petibmpy.read_field_hdf5(filepath, 'wz-avg')
    text.set_text('t = {}'.format(timestep * dt))
    if cont is not None:
        for collection in cont.collections:
            fig.gca().collections.remove(collection)
    cont = ax.contourf(x, y, wz, levels=levels, extend='both', zorder=0)
    filepath = figdir / 'wz_avg_wake2d_{:0>7}.png'.format(timestep)
    fig.savefig(filepath)
