from __future__ import print_function

import os
import subprocess

from h1st_pw.runtime import params

from h1st.IoT.PredMaint import __path__


cmd_args = [
    os.path.join(__path__[0], 'bin', 'h1st-iot-pm'),
    params.PROJECT,
    'conso-data',
    params.EQUIPMENT_GENERAL_TYPE, params.EQUIPMENT_UNIQUE_TYPE_GROUP,
    params.DATE
]

if params.TO_DATE:
    cmd_args += ['--to', params.TO_DATE]


cmd = ' '.join(cmd_args)

print('\n*** RUNNING {}... ***\n'.format(cmd))

subprocess.check_call(cmd_args)

print('\n*** {} DONE! ***\n'.format(cmd))
