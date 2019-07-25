from __future__ import print_function

import os
import subprocess
import sys

from arimo.IoT.PredMaint import __path__


PROJECT, EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP, DATE, TO_DATE = sys.argv[1:6]


cmd_args = [
    os.path.join(__path__[0], 'bin', 'arimo-iot-pm'),
    PROJECT,
    'agg-data',
    EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP,
    DATE
]

if TO_DATE and (TO_DATE != 'None'):
    cmd_args += ['--to', TO_DATE]


cmd = ' '.join(cmd_args)

print('\n*** RUNNING {}... ***\n'.format(cmd))

subprocess.check_call(cmd_args)

print('\n*** {} DONE! ***\n'.format(cmd))
