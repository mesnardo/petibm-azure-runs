import h5py


def petibm_read_grid(filepath, name):
    f = h5py.File(str(filepath), 'r')
    dim = len(f[name])
    x, y, z = f[name]['x'][:], f[name]['y'][:], None
    if dim == 3:
        z = f[name]['z'][:]
    f.close()
    if z is None or len(z) == 1:
        return x, y
    return x, y, z


def petibm_write_grid(filepath, name, *grid):
    labels = ('x', 'y', 'z')
    f = h5py.File(str(filepath), 'w')
    group = f.create_group(name)
    for i, gridline in enumerate(grid):
        group.create_dataset(labels[i], data=gridline)
    f.close()
    return