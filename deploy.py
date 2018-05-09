#!/usr/bin/env python


import argparse
import json
import os

from arimo.IoT.DataAdmin._project.settings import _DB_DETAILS_FILE_PATH


_DEFAULT_DB_DETAILS = json.load(open(_DB_DETAILS_FILE_PATH))


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--create', action='store_true')
arg_parser.add_argument('--env')

arg_parser.add_argument('--db-eng', default=_DEFAULT_DB_DETAILS['ENGINE'])
arg_parser.add_argument('--db-host', default=_DEFAULT_DB_DETAILS['HOST'])
arg_parser.add_argument('--db-port', default=_DEFAULT_DB_DETAILS['PORT'])
arg_parser.add_argument('--db-name', default=_DEFAULT_DB_DETAILS['NAME'])
arg_parser.add_argument('--db-usr', default=_DEFAULT_DB_DETAILS['USER'])
arg_parser.add_argument('--db-pw', default=_DEFAULT_DB_DETAILS['PASSWORD'])

args = arg_parser.parse_args()


json.dump(
    dict(ENGINE=args.db_eng,
         HOST=args.db_host,
         PORT=args.db_port,
         NAME=args.db_name,
         USER=args.db_usr,
         PASSWORD=args.db_pw),
    open(_DB_DETAILS_FILE_PATH, 'w'),
    indent=2)


os.system(
    'eb {} {}'.format(
        'create' if args.create else 'deploy',
        args.env))


json.dump(
    _DEFAULT_DB_DETAILS,
    open(_DB_DETAILS_FILE_PATH, 'w'),
    indent=2)
