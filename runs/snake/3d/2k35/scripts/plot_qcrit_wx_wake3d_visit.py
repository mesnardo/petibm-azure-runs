"""Visualize the contour of the z-component of the vorticity.

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
xdmf_path = simu_dir / 'output' / 'postprocessing' / 'qcrit_wx_cc.xmf'
config_view = simu_dir / 'scripts' / 'visit_view3d.yaml'
fig_dir = simu_dir / 'figures'
prefix = 'qcrit_wx_cc_wake3d_'

visit_plot_qcrit_wx_3d_direct(xdmf_path,
                              wx_range=(-5.0, 5.0),
                              q_value=1.0,
                              config_view=config_view,
                              out_dir=fig_dir, out_prefix=prefix,
                              figsize=(880, 372))
