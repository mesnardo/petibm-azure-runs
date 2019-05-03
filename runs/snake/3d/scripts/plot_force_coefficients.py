"""Plot the history of the force coefficients over time.

Save the figure in the sub-folder `figures`.
"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Calculate coefficient to convert force to force coefficient.
rho, u_inf = 1.0, 1.0  # density and freestream speed
dyn_pressure = 0.5 * rho * u_inf**2  # dynamic pressure
c = 1.0  # chord length
Lz = 3.2 * c  # spanwise length
coeff = 1 / (dyn_pressure * c * Lz)  # scaling factor for force coefficients

data = {}
folders = ['1k35', '2k15', '2k20', '2k25', '2k30', '2k35', '2k40']
maindir = pathlib.Path(__file__).absolute().parents[1]
for label in folders:
    simudir = maindir / label
    filepath = simudir / 'output' / 'forces-0.txt'
    t, fx, fy, fz = petibmpy.read_forces(filepath)
    nsteps = t.size
    # Check if there is a restarted simulation.
    simudir = maindir / (label + 'r')
    if simudir.is_dir():
        filepath2 = simudir / 'output' / 'forces-{}.txt'.format(nsteps)
        # Concatenate the histories.
        t, fx, fy, fz = petibmpy.read_forces(filepath, filepath2)
    # Compute the force coefficients.
    cd, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)
    # Compute the time-averaged force coefficients.
    cd_mean, cl_mean = petibmpy.get_time_averaged_values(t, cd, cl,
                                                         limits=(50.0, 100.0))
    print(label, cd_mean, cl_mean)
    subdata = {'t': t, 'cd': cd, 'cl': cl, 'cz': cz,
               'cd-mean': cd_mean, 'cl-mean': cl_mean}
    data[label] = subdata

# Save the time-averaged force coefficients into file.
datadir = maindir / 'data'
datadir.mkdir(parents=True, exist_ok=True)
filepath = datadir / 'timeAveragedForceCoefficients.csv'
with open(filepath, 'w') as outfile:
    outfile.write('Re,AoA,CD,CL,L/D\n')
    for label in folders:
        Re = 1000 * int(label[0])
        AoA = int(label[-2:])
        cd_mean, cl_mean = data[label]['cd-mean'], data[label]['cl-mean']
        ratio = cl_mean / cd_mean
        subdata = [Re, AoA, cd_mean, cl_mean, ratio]
        outfile.write(','.join([str(e) for e in subdata]) + '\n')

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(nrows=2, figsize=(8.0, 8.0))
ax[0].set_ylabel('Drag coefficient')
ax[0].grid()
for label, subdata in data.items():
    ax[0].plot(subdata['t'], subdata['cd'], label=label)
ax[0].legend(ncol=3)
ax[0].set_xlim(0.0, 100.0)
ax[0].set_ylim(-0.1, 3.0)
ax[1].set_xlabel('Non-dimensional time')
ax[1].set_ylabel('Lift coefficient')
ax[1].grid()
for label, subdata in data.items():
    ax[1].plot(subdata['t'], subdata['cl'], label=label)
ax[1].set_xlim(0.0, 100.0)
ax[1].set_ylim(-0.1, 3.0)
fig.tight_layout()

# Save the figure.
figdir = maindir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)

# Plot the time-averaged force coefficients.
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('Angle of attack (degrees)')
ax.set_ylabel('Time-averaged force coefficients')
ax.grid()
markers = {1000: 'x', 2000: 'o'}
for label, subdata in data.items():
    alpha = int(label[-2:])
    Re = 1000 * int(label[0])
    ax.scatter(alpha, subdata['cd-mean'], marker=markers[Re], color='C0')
    ax.scatter(alpha, subdata['cl-mean'], marker=markers[Re], color='C1')
ax.set_xlim(0.0, 50.0)
fig.tight_layout()

# Save the figure.
filepath = figdir / 'timeAveragedForceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
