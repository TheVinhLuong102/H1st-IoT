import os
import subprocess

from h1st_pw.runtime import params

from h1st.IoT.PredMaint import __path__


subprocess.check_call([
    os.path.join(__path__[0], 'bin', 'h1st-iot-pm'),
    params.PROJECT,
    'rm-s3-tmp'
])
