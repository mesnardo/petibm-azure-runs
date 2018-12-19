"""
Plots and saves the z-component of the 3D vorticity field
at given states.
"""

import os
import sys
import yaml
import argparse


# Parse command-line arguments.
parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = 'Plots the z-component of the vorticity field with VisIt.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--visit',
                    dest='visit_dir',
                    type=str,
                    default=None,
                    help='Path of VisIt.')
parser.add_argument('--arch',
                    dest='visit_arch',
                    type=str,
                    default='linux-x86_64',
                    help='Architecture.')
parser.add_argument('--wz-xdmf-path',
                    dest='wz_xdmf_path',
                    type=str,
                    required=True,
                    help='Path of the XDMF file for the z-vorticity.')
parser.add_argument('--body-p3d-paths',
                    dest='body_p3d_paths',
                    type=str,
                    nargs='+',
                    default=None,
                    help='Path of the Point3D files with the body coordinates.')
parser.add_argument('--state',
                    dest='state',
                    type=int,
                    default=None,
                    help='Single state index to plot.')
parser.add_argument('--states',
                    dest='states',
                    nargs='+',
                    type=int,
                    default=None,
                    help='State indices to plot.')
parser.add_argument('--states-range',
                    dest='states_range',
                    nargs=3,
                    type=int,
                    default=[0, None, 1],
                    help='Range to plot (start, end, step).')
parser.add_argument('--out-dir',
                    dest='out_dir',
                    type=str,
                    default=os.getcwd(),
                    help='Local directory where to save the figures.')
parser.add_argument('--out-prefix',
                    dest='out_prefix',
                    type=str,
                    default='wz_wake3d_',
                    help='Prefix to use for output file names.')
parser.add_argument('--view-config',
                    dest='config_view',
                    type=str,
                    default=None,
                    help='YAML file with 3D view parameters.')
parser.add_argument('--width',
                    dest='fig_width',
                    type=int,
                    default=1024,
                    help='Width of the figures to save (in pixels)')
parser.add_argument('--height',
                    dest='fig_height',
                    type=int,
                    default=1024,
                    help='Height of the figures to save (in pixels)')
args = parser.parse_args()

# Import VisIt package.
if args.visit_dir is None:
    try:
        args.visit_dir = os.environ['VISIT_DIR']
        print(args.visit_dir)
    except:
        raise ValueError('provide VisIt path with `--visit` or set VISIT_DIR')
sys.path.append(os.path.join(args.visit_dir, args.visit_arch,
                'lib', 'site-packages'))
from visit import *

LaunchNowin()

# Check version of VisIt.
script_version = '2.12.1'
tested_versions = [script_version, '2.13.2']
current_version = Version()
print('VisIt version: {}\n'.format(current_version))
if current_version not in tested_versions:
    print('[warning] You are using VisIt-{}.'.format(current_version))
    print('[warning] This script was created with VisIt-{}.'
          .format(script_version))
    print('[warning] This script was tested with versions: {}.'
          .format(tested_versions))
    print('[warning] It may not work as expected')

# Create database correlation with optional Point3D files.
num_bodies = 0
databases = [args.wz_xdmf_path]
if args.body_p3d_paths is not None:
    num_bodies = len(args.body_p3d_paths)
    databases = [path for path in args.body_p3d_paths]
    databases.append(args.wz_xdmf_path)
CreateDatabaseCorrelation('common', databases[num_bodies:], 0)

# Open the file with the coordinates of the immersed boundary.
if num_bodies > 0:
    for i in range(num_bodies):
        OpenDatabase(databases[i], 0, 'Point3D_1.0')
        # Add plot the mesh points.
        AddPlot('Mesh', 'points', 1, 1)
        # Set attributes of the mesh plot.
        MeshAtts = MeshAttributes()
        MeshAtts.legendFlag = 0
        MeshAtts.meshColor = (255, 204, 0, 1.0 * 255)
        MeshAtts.meshColorSource = MeshAtts.MeshCustom
        MeshAtts.pointSize = 0.05
        MeshAtts.pointType = MeshAtts.Point
        MeshAtts.pointSizePixels = 2
        MeshAtts.opacity = 1
        SetPlotOptions(MeshAtts)

# Open the XMF file for the z-component of the vorticity.
OpenDatabase(databases[-1], 0)
# Add the plot of the contour of the z-component of the vorticity.
AddPlot('Contour', 'wz', 1, 1)
# Set attributes of the contour.
ContourAtts = ContourAttributes()
ContourAtts.contourNLevels = 2
ContourAtts.SetMultiColor(0, (0, 51, 102, 0.6 * 255))
ContourAtts.SetMultiColor(1, (255, 0, 0, 0.6 * 255))
ContourAtts.legendFlag = 1
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -5.0
ContourAtts.max = 5.0
SetPlotOptions(ContourAtts)

# Parse the 3D view configuration file.
if args.config_view is not None:
    with open(args.config_view, 'r') as infile:
        config_view = yaml.load(infile)['View3DAtts']
# Set attributes of the view.
View3DAtts = View3DAttributes()
for key, value in config_view.items():
    if type(value) is list:
        value = tuple(value)
    setattr(View3DAtts, key, value)
SetView3D(View3DAtts)

# Remove time and user info.
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.axes3D.triadFlag = 1
AnnotationAtts.axes3D.bboxFlag = 0
SetAnnotationAttributes(AnnotationAtts)

DrawPlots()
SetActiveWindow(1)

Source(os.path.join(args.visit_dir, args.visit_arch, 'bin', 'makemovie.py'))
ToggleCameraViewMode()

# Create output directory if necessary.
if not os.path.isdir(args.out_dir):
    os.makedirs(args.out_dir)

# Loop over the states to render and save the plots.
if args.state is not None:
    states = [args.state]
elif args.states is not None:
    states = args.states
else:
    if args.states_range[1] is None:
        args.states_range[1] = TimeSliderGetNStates()
    else:
        args.states_range[1] += 1
    states = range(*args.states_range)

for state in states:
    print('[state {}] Rendering and saving figure ...'.format(state))
    SetTimeSliderState(state)

    RenderingAtts = RenderingAttributes()
    SetRenderingAttributes(RenderingAtts)

    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 0
    SaveWindowAtts.outputDirectory = args.out_dir
    SaveWindowAtts.fileName = '{}{:0>4}'.format(args.out_prefix, state)
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.PNG
    SaveWindowAtts.width = 1024
    SaveWindowAtts.height = 1024
    SaveWindowAtts.quality = 100
    SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
    SetSaveWindowAttributes(SaveWindowAtts)

    SaveWindow()

os.remove('visitlog.py')
sys.exit(0)
