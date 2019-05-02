"""
Generate a figure of the force coefficients over time.
Save the figure in the sub-folder `figures` of the simulation directory.
"""

import sys
import pathlib
from matplotlib import pyplot

root_dir = pathlib.Path(__file__).absolute().parents[6]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc


simu_dir = pathlib.Path(__file__).absolute().parents[1]

# Read forces for both bodies and convert to force coefficients.
filepath = simu_dir / 'output' / 'forces-0.txt'
t, fx1, fy1, fz1, fx2, fy2, fz2 = misc.petibm_read_forces(filepath)
rho, u_inf = 1.0, 1.0  # density and freestream speed
dyn_pressure = 0.5 * rho * u_inf**2  # dynamic pressure
c = 1.0  # chord length
Lz = 3.2 * c  # spanwise length
coeff = 1 / (dyn_pressure * c * Lz)  # scaling factor for force coefficients
cd1, cl1, cz1 = misc.get_force_coefficients(fx1, fy1, fz1, coeff=coeff)
cd2, cl2, cz2 = misc.get_force_coefficients(fx2, fy2, fz2, coeff=coeff)

pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd1, label='$C_D$ (upstream)')
ax.plot(t, cl1, label='$C_L$ (upstream)')
ax.plot(t, cz1, label='$C_z$ (upstream)')
ax.plot(t, cd2, label='$C_D$ (downstream)')
ax.plot(t, cl2, label='$C_L$ (downstream)')
ax.plot(t, cz2, label='$C_z$ (downstream)')
ax.legend(ncol=2, prop={'size': 14})
ax.set_xlim(t[0], t[-1])
ax.set_ylim(-0.1, 3.5)
fig.tight_layout()

fig_dir = simu_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
