from setuptools import find_packages, setup
import six


install_requires = []
for s in open('requirements.txt').readlines():
    if not s.startswith('#'):
        s = s.strip()
        lower_s = s.lower()
        install_requires.append(
            'Django >= 1.11.27, < 2'   # last 1.x ver compat w/ Py2
            if lower_s.startswith('django ')
            else ('Django-AutoComplete-Light >= 3.2.10, < 3.3'   # last 3.2.x ver compat w/ Py2
                  if six.PY2 and lower_s.startswith('django-autocomplete-light')
                  else ('DjangoRESTFramework-Filters >= 0.11.1, < 1'   # last 0.x ver compat w/ Py2
                        if six.PY2 and lower_s.startswith('djangorestframework-filters')
                        else ('DjangoRESTFramework >= 3.9.4'   # last 3.9 ver compat w/ Py2
                              if six.PY2 and lower_s.startswith('djangorestframework')
                              else ('Django-Filter >= 1.1.0, < 2'   # last 1.x ver compat w/ Py2
                                    if six.PY2 and lower_s.startswith('django-filter')
                                    else ('Django-Silk >= 3.0.4, < 4'   # last 3.x ver compat w/ Py2
                                          if six.PY2 and lower_s.startswith('django-silk')
                                          else s))))))


setup(
    name='Arimo-PredMaint',
    author='Arimo',
    author_email='DSAR@Arimo.com',
    url='https://github.com/adatao/PredMaint',
    version='0.0.0',
    description='Arimo Predictive Maintenance',
    long_description='Arimo Predictive Maintenance',
    keywords='Arimo Predictive Maintenance',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    scripts=['bin/arimo-pm'])
