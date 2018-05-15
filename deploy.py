import argparse
import os
from ruamel import yaml
import shutil

from arimo.IoT.DataAdmin import Project, _YAML_EXT
from arimo.IoT.DataAdmin._project.settings import _DB_DETAILS_FILE_PATH


IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH = _DB_DETAILS_FILE_PATH + '.orig'

assert not os.path.isfile(IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH)


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--create', action='store_true')
arg_parser.add_argument('--project', default='TEST')

args = arg_parser.parse_args()


iot_dataadmin_db_details_file_path = \
    os.path.join(
        Project.CONFIG_DIR_PATH,
        args.project + _YAML_EXT)

iot_dataadmin_db_details = \
    yaml.safe_load(stream=os.path.isfile(iot_dataadmin_db_details_file_path))['db']['admin']

assert iot_dataadmin_db_details['host'] \
   and iot_dataadmin_db_details['db_name'] \
   and iot_dataadmin_db_details['user'] \
   and iot_dataadmin_db_details['password']


shutil.copyfile(
    src=_DB_DETAILS_FILE_PATH,
    dst=IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH)

assert os.path.isfile(IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH)


shutil.copyfile(
    src=iot_dataadmin_db_details_file_path,
    dst=_DB_DETAILS_FILE_PATH)

os.system(
    'eb {} {}'.format(
        'create' if args.create else 'deploy',
        args.project))


shutil.copyfile(
    src=IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH,
    dst=_DB_DETAILS_FILE_PATH)

os.remove(path=IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH)

assert not os.path.isfile(IoT_DATA_ADMIN_DB_DETAILS_ORIG_FILE_PATH)
