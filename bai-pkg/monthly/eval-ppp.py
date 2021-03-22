from __future__ import print_function

import os
import subprocess
import sys

from h1st.IoT.PredMaint import __path__


PROJECT = sys.argv[1]


cmd_args = [
    os.path.join(__path__[0], 'bin', 'h1st-iot-pm'),
    PROJECT,
    'eval-ppp'
]


cmd = ' '.join(cmd_args)

print('\n*** RUNNING {}... ***\n'.format(cmd))

subprocess.check_call(cmd_args)

print('\n*** {} DONE! ***\n'.format(cmd))
