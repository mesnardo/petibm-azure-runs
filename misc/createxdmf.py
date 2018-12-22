#!/usr/bin/env python
"""
Creates an XMF file for the x-component of the velocity field.
"""

import sys
import pathlib
from lxml import etree

from .grid import petibm_read_grid


def petibm_write_xdmf(outpath, data_dir, gridpath, name,
                      nstart, nt, nsave, dt):
    # Initialize XDMF file.
    xdmf = etree.Element('Xdmf', Version='2.2')
    info = etree.SubElement(xdmf, 'Information',
                            Name='MetaData',
                            Value='ID-23454')
    domain = etree.SubElement(xdmf, 'Domain')
    grid_time_series = etree.SubElement(domain, 'Grid',
                                        Name='TimeSeries',
                                        GridType='Collection',
                                        CollectionType='Temporal')
    # Read grid to get dimension and number of points.
    grid = petibm_read_grid(gridpath, name)
    dim = len(grid)
    topology_type = '{}DRectMesh'.format(dim)
    geometry_type = 'VXVY' + (dim == 3) * 'VZ'
    components = ('x', 'y', 'z')[:dim]
    gridsize = [len(line) for line in grid]
    number_of_elements = ' '.join(str(n) for n in gridsize[::-1])
    precision = '8'
    # Get time-step indices and time values.
    states = list(range(nstart, nstart + nt + 1, nsave))
    times = [state * dt for state in states]
    # Generate the time series.
    for state, time in zip(states, times):
        grid = etree.SubElement(grid_time_series, 'Grid',
                                Name='Grid',
                                GridType='Uniform')
        time = etree.SubElement(grid, 'Time', Value=str(time))
        topology = etree.SubElement(grid, 'Topology',
                                    TopologyType=topology_type,
                                    NumberOfElements=number_of_elements)
        geometry = etree.SubElement(grid, 'Geometry',
                                    GeometryType=geometry_type)
        # Create XDMF block for the grid. (Use of loop for code-reuse.)
        for component, n in zip(components, gridsize):
            dataitem = etree.SubElement(geometry, 'DataItem',
                                        Dimensions=str(n),
                                        NumberType='Float',
                                        Precision=precision,
                                        Format='HDF')
            dataitem.text = ':/'.join([str(gridpath), name + '/' + component])
        # Create XDMF block for the scalar field variable.
        attribute = etree.SubElement(grid, 'Attribute',
                                     Name=name,
                                     AttributeType='Scalar',
                                     Center='Node')
        dataitem = etree.SubElement(attribute, 'DataItem',
                                    Dimensions=number_of_elements,
                                    NumberType='Float',
                                    Precision=precision,
                                    Format='HDF')
        filepath = data_dir / '{:0>7}.h5'.format(state)
        dataitem.text = ':/'.join([str(filepath), name])
    # Write XDMF file.
    tree = etree.ElementTree(xdmf)
    tree.write(str(outpath), pretty_print=True, xml_declaration=True)
    return