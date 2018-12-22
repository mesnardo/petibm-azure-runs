"""
Generate figures of the 2D pseudocolor of the spanwise-averaged z-component
of the 3D vorticity field.
"""

import os
import sys
import pathlib

root_dir = pathlib.Path(__file__).absolute().parents[5]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc


simu_dir = pathlib.Path(__file__).absolute().parents[1]
xdmf_path = simu_dir / 'output' / 'postprocessing' / 'wz_avg' / 'wz-avg.xmf'
name = 'wz-avg'
config_view = simu_dir / 'scripts' / 'visit_view2d.yaml'
curve2d_path = simu_dir / 'output' / 'snake2d40.curve'
fig_dir = simu_dir / 'figures'
prefix = 'wz_avg_wake2d_'

misc.visit_plot_pseudocolor_2d(xdmf_path, name,
                               value_range=(-5.0, 5.0),
                               curve2d_paths=[curve2d_path],
                               config_view=config_view,
                               out_dir=fig_dir, out_prefix=prefix,
                               figsize=(1024, 1024),
                               visit_dir=os.environ.get('VISIT_DIR'))
