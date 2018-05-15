import argparse
import os
from ruamel import yaml

from arimo.IoT.DataAdmin import Project, _YAML_EXT
from arimo.IoT.DataAdmin._project.settings import _DB_DETAILS_FILE_PATH


_DEFAULT_IoT_DATA_ADMIN_DB_DETAILS = \
    yaml.safe_load(open(_DB_DETAILS_FILE_PATH, 'r'))


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--create', action='store_true')
arg_parser.add_argument('--project', default='TEST')

args = arg_parser.parse_args()


iot_dataadmin_db_details = \
    yaml.safe_load(
        open(os.path.join(
                Project.CONFIG_DIR_PATH,
                args.project + _YAML_EXT),
             'r'))['db']['admin']


yaml.safe_dump(
    data=dict(
        ENGINE=_DEFAULT_IoT_DATA_ADMIN_DB_DETAILS['ENGINE'],
        HOST=iot_dataadmin_db_details['host'],
        PORT=_DEFAULT_IoT_DATA_ADMIN_DB_DETAILS['PORT'],
        NAME=iot_dataadmin_db_details['name'],
        USER=iot_dataadmin_db_details['user'],
        PASSWORD=iot_dataadmin_db_details['password']),
    stream=open(_DB_DETAILS_FILE_PATH, 'w'),
    default_style=None,
    default_flow_style=False,   # collections to be always serialized in the block style
    canonical=None,
    indent=2,
    width=None,
    allow_unicode=True,
    line_break=None,
    encoding=u'utf-8',
    explicit_start=None,
    explicit_end=None,
    version=None,
    tags=None,
    block_seq_indent=None)


os.system(
    'eb {} {}'.format(
        'create' if args.create else 'deploy',
        args.project))


yaml.safe_dump(
    data=_DEFAULT_IoT_DATA_ADMIN_DB_DETAILS,
    stream=open(_DB_DETAILS_FILE_PATH, 'w'),
    default_style=None,
    default_flow_style=False,   # collections to be always serialized in the block style
    canonical=None,
    indent=2,
    width=None,
    allow_unicode=True,
    line_break=None,
    encoding=u'utf-8',
    explicit_start=None,
    explicit_end=None,
    version=None,
    tags=None,
    block_seq_indent=None)
