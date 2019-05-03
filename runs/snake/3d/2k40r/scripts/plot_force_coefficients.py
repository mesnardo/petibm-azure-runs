"""Plot the history of the force coefficients.

The Matplotlib figure is saved in the sub-folder `figures`
of the direction simulation directory.
"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[2]

# Load the history of the forces.
prevdir = rootdir / '2k40'
filepath1 = prevdir / 'output' / 'forces-0.txt'
simudir = rootdir / '2k40r'
filepath2 = simudir / 'output' / 'forces-100000.txt'
t, fx, fy, fz = petibmpy.read_forces(filepath1, filepath2)

# Compute the history of the force coefficients.
rho, u_inf = 1.0, 1.0  # density and freestream speed
dyn_pressure = 0.5 * rho * u_inf**2  # dynamic pressure
c = 1.0  # chord length
Lz = 3.2 * c  # spanwise length
coeff = 1 / (dyn_pressure * c * Lz)  # scaling factor for force coefficients
cd, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.plot(t, cz, label='$C_z$')
ax.legend(ncol=3)
ax.set_xlim(t[0], t[-1])
ax.set_ylim(-0.1, 3.0)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
