"""
Generate a figure of the drag and lift force coefficients over time.
Save the figure in the sub-folder `figures` of the simulation directory.
"""

import sys
import pathlib
from matplotlib import pyplot

root_dir = pathlib.Path(__file__).absolute().parents[5]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc


simu_dir = pathlib.Path(__file__).absolute().parents[1]

filepath = simu_dir / 'output' / 'forces-0.txt'
t, fx, fy = misc.petibm_read_forces(filepath)
cd, cl = misc.get_force_coefficients(fx, fy, coeff=2.0)

pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.legend()
ax.set_xlim(t[0], t[-1])
ax.set_ylim(0.0, 3.0)
fig.tight_layout()

fig_dir = simu_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
