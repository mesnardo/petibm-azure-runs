"""Plot the history of the force coefficients.

The Matplotlib figure is saved in the sub-folder `figures`
of the direction simulation directory.
"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Load the history of the forces.
maindir = pathlib.Path(__file__).absolute().parents[2]
simudir = maindir / '2k25-stagger0'
filepath1 = simudir / 'output' / 'forces-0.txt'
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath2 = simudir / 'output' / 'forces-50000.txt'
t, fx1, fy1, fz1, fx2, fy2, fz2 = petibmpy.read_forces(filepath1, filepath2)

# Compute the history of the force coefficients.
rho, u_inf = 1.0, 1.0  # density and freestream speed
dyn_pressure = 0.5 * rho * u_inf**2  # dynamic pressure
c = 1.0  # chord length
Lz = 3.2 * c  # spanwise length
coeff = 1 / (dyn_pressure * c * Lz)  # scaling factor for force coefficients
cd1, cl1, cz1 = petibmpy.get_force_coefficients(fx1, fy1, fz1, coeff=coeff)
cd2, cl2, cz2 = petibmpy.get_force_coefficients(fx2, fy2, fz2, coeff=coeff)

# Plot the history of the force coefficients.
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

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
