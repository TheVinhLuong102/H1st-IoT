import os
import subprocess

from arimo_pw.runtime import params

from arimo.IoT.PredMaint import __path__


subprocess.check_call([
    os.path.join(__path__[0], 'bin', 'arimo-iot-pm'),
    params.PROJECT,
    'rm-s3-tmp'
])
