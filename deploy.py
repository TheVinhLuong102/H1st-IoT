#!/usr/bin/env python


import argparse
import json
import os

from arimo.IoT.DataAdmin._project.settings import _DB_DETAILS_FILE_PATH


_DEFAULT_DB_DETAILS = json.load(open(_DB_DETAILS_FILE_PATH))


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--eb-env', default='ArimoIoTDataAdmin-env')

arg_parser.add_argument('--db-eng', default='django.db.backends.postgresql')
arg_parser.add_argument('--db-host')
arg_parser.add_argument('--db-port', default='5432')
arg_parser.add_argument('--db-name')
arg_parser.add_argument('--db-usr')
arg_parser.add_argument('--db-pw')

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


os.system('eb create {}'.format(args.eb_env))


json.dump(_DEFAULT_DB_DETAILS, open(_DB_DETAILS_FILE_PATH, 'w'), indent=2)
