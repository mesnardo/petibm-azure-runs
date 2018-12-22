import h5py


def petibm_read_field(filepath, name):
    f = h5py.File(str(filepath), 'r')
    field = f[name][:]
    f.close()
    return field


def petibm_write_field(filepath, name, field):
    f = h5py.File(str(filepath), 'w')
    f.create_dataset(name, data=field)
    f.close()
    return
