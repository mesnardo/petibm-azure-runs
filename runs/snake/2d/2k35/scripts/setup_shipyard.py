import os
import sys
import argparse
import pathlib


root_dir = pathlib.Path(__file__).absolute().parents[5]
if root_dir not in sys.path:
    sys.path.insert(0, str(root_dir))
import misc


def parse_command_line():
    """
    Parses the command-line options.
    """
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    description = 'Batch Shipyard: setup the configuration files.'
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter_class)
    parser.add_argument('--resource-group', dest='resource_group',
                        type=str,
                        required=True,
                        help='Name of resource group.')
    parser.add_argument('--account-name', dest='account_name',
                        type=str,
                        required=True,
                        help='Storage account name.')
    parser.add_argument('--share-name', dest='share_name',
                        type=str,
                        required=True,
                        help='Storage fileshare name.')
    args = parser.parse_args()
    return args


args = parse_command_line()
info = {}
info['<resource-group>'] = args.resource_group
info['<location>'] = misc.get_resource_group_location(args.resource_group)
info['<subscription-id>'], info['<tenant-id>'] = misc.get_subscription_ids()
info['<username>'] = misc.get_username()
info['<batch-account-name>'] = misc.get_batch_account_name(args.resource_group)
url = 'https://' + misc.get_batch_account_endpoint(args.resource_group)
info['<batch-account-service-url>'] = url
info['<storage-account-name>'] = args.account_name
key = misc.get_storage_account_key(args.resource_group, args.account_name)
info['<storage-account-key>'] = key
info['<storage-share-name>'] = args.share_name

root_dir = pathlib.Path(__file__).absolute().parents[5]
simu_dir = pathlib.Path(__file__).absolute().parents[1]

inpath = root_dir / 'misc' / 'run-petibm-template.sh'
outpath = simu_dir / 'run-petibm.sh'
misc.replace_strings_in_file(inpath, info, output=outpath)
os.chmod(outpath, 0o777)

inpath = root_dir / 'misc' / 'credentials-template.yaml'
outpath = simu_dir / 'config_shipyard' / 'credentials.yaml'
misc.replace_strings_in_file(inpath, info, output=outpath)
