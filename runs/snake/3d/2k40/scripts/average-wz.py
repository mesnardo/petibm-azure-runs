"""
Average the spanwise vorticity field along the spanwise direction and write the
2D field values into HDF5 file.
"""

import sys
import pathlib
import numpy
import yaml

root_dir = pathlib.Path(__file__).absolute().parents[5]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc


name = 'wz'  # name of the field variable

# Get directories.
simu_dir = pathlib.Path(__file__).absolute().parents[1]
data_dir = simu_dir / 'output' / 'solution'
out_dir = simu_dir / 'output' / 'postprocessing' / (name + '_avg')
out_dir.mkdir(parents=True, exist_ok=True)

# Read 3D grid and write 2D grid.
gridpath = simu_dir / 'output' / 'grid.h5'
x, y, _ = misc.petibm_read_grid(gridpath, name)
gridpath = out_dir / 'grid.h5'
misc.petibm_write_grid(gridpath, name + '-avg', x, y)

# Get temporal parameters.
filepath = simu_dir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile)['parameters']
nstart, nt, nsave = config['startStep'], config['nt'], config['nsave']
dt = config['dt']
timesteps = list(range(nstart, nstart + nt + 1, nsave))

# Average the scalar field along the z-direction and write field.
for timestep in timesteps:
    print('[time step {}]'.format(timestep))
    filepath = data_dir / '{:0>7}.h5'.format(timestep)
    data = misc.petibm_read_field(filepath, name)
    data_avg = numpy.mean(data, axis=0)
    filepath = out_dir / '{:0>7}.h5'.format(timestep)
    misc.petibm_write_field(filepath, name + '-avg', data_avg)

# Write XDMF file to visualize field with VisIt.
filepath = out_dir / (name + '-avg.xmf')
misc.petibm_write_xdmf(filepath, out_dir, gridpath, name + '-avg',
                       nstart, nt, nsave, dt)
