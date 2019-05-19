"""Generate the YAML node 'mesh' with details of the Cartesian grid."""

import math
import numpy
import pathlib

import petibmpy


# Info about the 3D structured Cartesian grid.
width = 0.008  # minimum grid spacing in the x- and y- directions
chord = 1.0  # chord-length of the body cross-section
spanwise_width = 10.0 * width  # grid-spacing in the spanwise direction
spanwise_length = 3.2 * chord  # target spanwise length
spanwise_cells = math.ceil(spanwise_length / spanwise_width)  # cells required
spanwise_length = spanwise_cells * spanwise_width  # actual spanwise length
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
                         'stretchRatio': ratio}]},
        {'direction': 'z', 'start': 0.0,
         'subDomains': [{'end': spanwise_length,
                         'width': spanwise_width,
                         'stretchRatio': 1.0}]}]

mesh = petibmpy.CartesianGrid(info)
print(mesh)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml(filepath, ndigits=10)
