"""Create a single XDMF file for the Q-criterion and the x-vorticity."""

import pathlib
import yaml

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]
simudir = simudir / 'output'
outdir = simudir / 'postprocessing'
outdir.mkdir(parents=True, exist_ok=True)

# Get temporal parameters.
filepath = simudir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)['parameters']
nstart, nt, nsave = config['startStep'], config['nt'], config['nsave']
timesteps = list(range(nstart, nstart + nt + 1, nsave))

# Write the XDMF file to visualize with VisIt.
filepath = outdir / 'qcrit_wx_cc.xmf'
config = {'grid': outdir / 'qcrit' / 'grid.h5',
          'data': {'qcrit': outdir / 'qcrit',
                   'wx_cc': outdir / 'wx_cc'}}
petibmpy.write_xdmf_multi(filepath, config, states=timesteps)
