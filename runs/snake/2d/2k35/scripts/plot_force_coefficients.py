import pathlib
import numpy
from matplotlib import pyplot


def read_forces(filepath):
    with open(filepath, 'r') as infile:
        data = numpy.loadtxt(infile, unpack=True)
    return data


simu_dir = pathlib.Path(__file__).absolute().parents[1]

simus = {}

label = 'PetIBM-0.4 (Azure)'
filepath = simu_dir / 'output' / 'forces-0.txt'
t, fx, fy = read_forces(filepath)
simus[label] = {'t': t, 'cd': 2 * fx, 'cl': 2 * fy}

label = 'PetIBM-0.3.1 (Colonial One)'
filepath = simu_dir / 'data' / 'forces-0-prev.txt'
t, fx, fy = read_forces(filepath)
simus[label] = {'t': t, 'cd': 2 * fx, 'cl': 2 * fy}

pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(nrows=2, figsize=(6.0, 6.0), sharex=True)
for i, coeff in enumerate(['cd', 'cl']):
    ax[i].set_ylabel('${}_{}$'.format(*coeff.upper()))
    ax[i].grid()
    for label, data in simus.items():
        ax[i].plot(data['t'], data[coeff], label=label)
    ax[i].legend()
ax[0].set_xlabel('$t$')
ax[0].set_xlim(t[0], t[-1])
ax[0].set_ylim(0.0, 2.5)
ax[1].set_ylim(1.0, 3.0)

pyplot.show()
