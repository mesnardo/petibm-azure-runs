"""Visualize the pseudocolor of the z-averaged z-component of the vorticity.

The figures are generated with VisIt and saved in the sub-folder `figures`
of the simulation directory.
"""

import os
import pathlib
import sys

petibmpy_dir = os.environ.get('PETIBMPY_DIR')
if petibmpy_dir is None:
    raise ValueError('Set environment variable PETIBMPY_DIR')
sys.path.insert(0, os.path.join(petibmpy_dir, 'misc'))
from visitplot import *


simu_dir = pathlib.Path(__file__).absolute().parents[1]
xdmf_path = simu_dir / 'output' / 'postprocessing' / 'wz_avg' / 'wz-avg.xmf'
name = 'wz-avg'
config_view = simu_dir / 'scripts' / 'visit_view2d.yaml'
curve2d_path = simu_dir / 'output' / 'snake2d40.curve'
fig_dir = simu_dir / 'figures'
prefix = 'wz_avg_wake2d_'

visit_plot_pseudocolor_2d(xdmf_path, name,
                          value_range=(-5.0, 5.0),
                          curve2d_paths=[curve2d_path],
                          config_view=config_view,
                          out_dir=fig_dir, out_prefix=prefix,
                          figsize=(1024, 1024))
