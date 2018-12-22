"""
Functions to read forces from file and convert them to force coefficients.
"""


import numpy


def petibm_read_forces(filepath):
    """
    Read PetIBM forces from given file.

    Arguments
    ---------
    filepath: str or pathlib.Path object
        Path of the file to read.

    Returns
    -------
    data: tuple of 4 numpy.ndarray objects
        Time followed by the forces in the x, y, and z directions.
    """
    with open(filepath, 'r') as infile:
        data = numpy.loadtxt(infile, unpack=True)
    return data


def get_force_coefficients(*forces, **kwargs):
    """
    Convert forces to force coefficients.

    Arguments
    ---------
    forces: tuple of numpy.ndarray objects
        The forces.
    coeff: float (optional)
        The scaling coefficient;
        default: 1.0.

    Returns
    -------
    force_coeffs: tuple of numpy.ndarray objects
        The force coefficients.
    """
    coeff = kwargs['coeff']
    force_coeffs = (coeff * f for f in forces)
    return force_coeffs
