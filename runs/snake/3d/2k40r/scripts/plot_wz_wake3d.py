"""
Generate figures of the 3D contour of the z-component of the vorticity field.
"""

import os
import sys
import pathlib

root_dir = pathlib.Path(__file__).absolute().parents[5]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc


simu_dir = pathlib.Path(__file__).absolute().parents[1]
xdmf_path = simu_dir / 'output' / 'wz.xmf'
name = 'wz'
config_view = simu_dir / 'scripts' / 'visit_view3d.yaml'
p3d_path = simu_dir / 'output' / 'snake3d40.p3d'
fig_dir = simu_dir / 'figures'
prefix = 'wz_wake3d_'

misc.visit_plot_contour_3d(xdmf_path, name,
                           value_range=(-5.0, 5.0),
                           p3d_paths=[p3d_path],
                           config_view=config_view,
                           out_dir=fig_dir, out_prefix=prefix,
                           figsize=(1024, 1024),
                           visit_dir=os.environ.get('VISIT_DIR'))
