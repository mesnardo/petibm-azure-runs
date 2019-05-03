"""Plot the history of the force coefficients over time.

The Matplotlib figure is saved in the `figures` sub-folder
of the simulation directory.
"""

from matplotlib import pyplot
import pathlib

import petibmpy


# Load the history of the forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'output' / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)
# Convert to force coefficients.
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=2.0)

# Plot the history of the force coefficients.
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

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
