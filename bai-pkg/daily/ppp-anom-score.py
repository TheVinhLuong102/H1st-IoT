from __future__ import print_function

from datetime import date, timedelta
import os
import subprocess
import sys

from h1st.IoT.PredMaint import __path__


PROJECT, EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP = sys.argv[1:4]


today = date.today()

cmd_args = [
    os.path.join(__path__[0], 'bin', 'h1st-iot-pm'),
    PROJECT,
    'ppp-anom-score',
    EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP,
    str(today - timedelta(days=30)), '--to', str(today)
]


cmd = ' '.join(cmd_args)

print('\n*** RUNNING {}... ***\n'.format(cmd))

subprocess.check_call(cmd_args)

print('\n*** {} DONE! ***\n'.format(cmd))
