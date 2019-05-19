"""Generate the YAML node 'mesh' with details of the Cartesian grid."""

import numpy
import pathlib

import petibmpy


# Info about the 2D structured Cartesian grid.
width = 0.004  # minimum grid spacing in the x- and y- directions
ratio = 1.01  # stretching ratio
info = [{'direction': 'x', 'start': -15.0,
         'subDomains': [{'end': -0.52,
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True},
                        {'end': 3.48,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': ratio}]},
        {'direction': 'y', 'start': -15.0,
         'subDomains': [{'end': -2.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True},
                        {'end': 2.0,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': ratio}]}]

mesh = petibmpy.CartesianGrid(info)
print(mesh)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml(filepath, ndigits=10)
