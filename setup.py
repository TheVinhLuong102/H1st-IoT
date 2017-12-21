import json
import os
from setuptools import find_packages, setup


_PACKAGE_NAMESPACE_NAME = 'arimo'

_METADATA_FILE_NAME = 'metadata.json'

_REQUIREMENTS_FILE_NAME = 'requirements.txt'


_metadata = \
    json.load(
        open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            _PACKAGE_NAMESPACE_NAME,
            _METADATA_FILE_NAME)))

try:
    import arimo.metadata
    _metadata['VERSION'] = arimo.metadata.VERSION
except ImportError:
    pass


setup(
    name=_metadata['PACKAGE'],
    author=_metadata['AUTHOR'],
    author_email=_metadata['AUTHOR_EMAIL'],
    url=_metadata['URL'],
    version=_metadata.get('VERSION'),
    description=_metadata['DESCRIPTION'],
    long_description=_metadata['DESCRIPTION'],
    keywords=_metadata['DESCRIPTION'],
    packages=find_packages(),
    install_requires=
        [s.strip()
         for s in open(_REQUIREMENTS_FILE_NAME).readlines()
         if s.startswith('#')])
