import json
import os
from setuptools import find_packages, setup


_PACKAGE_NAMESPACE_NAME = 'arimo'

_METADATA_FILE_NAME = 'metadata.json'

_REQUIREMENTS_FILE_NAME = 'requirements.txt'


_metadata = \
    json.load(
        open(os.path.join(
            os.path.dirname(__file__),
            _PACKAGE_NAMESPACE_NAME,
            _METADATA_FILE_NAME)))


_SCRIPT_REL_PATH_TO_INSTALL = 'bin/arimo-iot-data'


setup(
    name=_metadata['PACKAGE'],
    author=_metadata['AUTHOR'],
    author_email=_metadata['AUTHOR_EMAIL'],
    url=_metadata['URL'],
    version=_metadata['VERSION'],
    description=_metadata['DESCRIPTION'],
    long_description=_metadata['DESCRIPTION'],
    keywords=_metadata['DESCRIPTION'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=
        [s.strip()
         for s in open(_REQUIREMENTS_FILE_NAME).readlines()
         if not s.startswith('#')],
    scripts=[_SCRIPT_REL_PATH_TO_INSTALL])


for _dir_path in (os.path.expanduser('~/.local'), '/usr/local'):
    _bin_dir_path = os.path.join(_dir_path, 'bin')

    if not os.path.isdir(_bin_dir_path):
        os.makedirs(_bin_dir_path)

    _executable_script_path = \
        os.path.join(
            _dir_path,
            _SCRIPT_REL_PATH_TO_INSTALL)

    if not (os.path.isfile(_executable_script_path) or os.path.islink(_executable_script_path)):
        os.symlink(
            os.path.join(os.path.dirname(__file__), _SCRIPT_REL_PATH_TO_INSTALL),
            _executable_script_path)

    assert os.path.isfile(_executable_script_path) or os.path.islink(_executable_script_path)
