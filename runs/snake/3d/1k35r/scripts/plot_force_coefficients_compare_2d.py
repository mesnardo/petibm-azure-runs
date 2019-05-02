"""
Generate a figure of the force coefficients over time.
Compare the 3D force coefficients with the 2D ones.
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

# Read 3D forces and convert to force coefficients.
filepath = simu_dir / 'output' / 'forces-0.txt'
t, fx, fy, fz = misc.petibm_read_forces(filepath)
rho, u_inf = 1.0, 1.0  # density and freestream speed
dyn_pressure = 0.5 * rho * u_inf**2  # dynamic pressure
c = 1.0  # chord length
Lz = 3.2 * c  # spanwise length
coeff = 1 / (dyn_pressure * c * Lz)  # scaling factor for force coefficients
cd, cl, cz = misc.get_force_coefficients(fx, fy, fz, coeff=coeff)

# Read 2D forces and convert to force coefficients.
filepath = simu_dir / 'data' / 'forces-2d-prev.txt'
t2, fx2, fy2 = misc.petibm_read_forces(filepath)
coeff = 1 / (dyn_pressure * c)
cd2, cl2 = misc.get_force_coefficients(fx2, fy2, coeff=coeff)

# Plot force coefficients over time.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.plot(t2, cd2, label='$C_D$ (2D)', color='grey', linestyle='-')
ax.plot(t2, cl2, label='$C_L$ (2D)', color='grey', linestyle='--')
ax.legend(ncol=2)
ax.set_xlim(t[0], t[-1])
ax.set_ylim(0.55, 3.5)
fig.tight_layout()

# Save figure as PNG file.
fig_dir = simu_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'forceCoefficientsCompare2D.png'
fig.savefig(str(filepath), dpi=300)
