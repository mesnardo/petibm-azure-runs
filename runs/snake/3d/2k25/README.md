# 3D flow around a snake cylinder (Re=2000, AoA=25deg)

All commands are run from the directory that contains the present README file.

To create the file containing the coordinates of the immersed boundary for the snake cylinder:

```bash
python scripts/create_body.py
```

Output: `snake3d25.body`.

To visualize the 3D geometry:

```
sed '1d' snake3d25.body > snake.3D
```

then open the file with VisIt with Point3D format.

To create the YAML node `mesh` (that contains information about the structured Cartesian grid):

```bash
python scripts/create_mesh_yaml.py
```

Output: `mesh.yaml` (content to be placed into the global YAML configuration file `config.yaml`).

To setup your Azure credentials in the Batch Shipyard configuration file `credentials.yaml`:

```bash
python scripts/setup_shipyard.py --resource-group <resource-group> --storage-account-name <storage-accout-name> --share-name <storage-fileshare-name>
```

Outputs: `config_shipyard/credentials.yaml` and `run-petibm.sh`.

To submit the simulation to Azure Batch:

```bash
./shipard-driver.sh
```

The Shell script will ask you to provide the path of the configuration directory for Batch Shipyard (which is `config_shipyard`) and your Microsoft Azure password.

To download locally the simulation data from Azure Storage:

```bash
mkdir output
az storage file download-batch --source myfileshare/snake3d2k25/ --destination output --account-name <storage-account-name>
```
