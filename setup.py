import json
import os
from setuptools import find_packages, setup
import six


_PACKAGE_NAMESPACE_NAME = 'arimo'

_METADATA_FILE_NAME = 'metadata.json'

_REQUIREMENTS_FILE_NAME = 'requirements.txt'


_metadata = \
    json.load(
        open(os.path.join(
            os.path.dirname(__file__),
            _PACKAGE_NAMESPACE_NAME,
            _METADATA_FILE_NAME)))


install_requires = []

for s in open(_REQUIREMENTS_FILE_NAME).readlines():
    if not s.startswith('#'):
        s = s.strip()
        lower_s = s.lower()
        install_requires.append(
            'Django'
            if lower_s.startswith('django >=')
            else ('Django-AutoComplete-Light == 3.2.10'
                  if six.PY2 and lower_s.startswith('django-autocomplete-light')
                  else ('DjangoRESTFramework-Filters == 0.10.2'
                        if six.PY2 and lower_s.startswith('djangorestframework-filters')
                        else ('Django-Filter == 1.1.0'
                              if six.PY2 and lower_s.startswith('django-filter')
                              else s))))

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
    install_requires=install_requires)
