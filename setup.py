from setuptools import find_namespace_packages, setup


setup(
    name='Arimo-PredMaint',
    author='Arimo LLC',
    author_email='DSAR@Arimo.com',
    url='https://github.com/adatao/PredMaint',
    version='0.0.0',
    description='Arimo Predictive Maintenance',
    long_description='Arimo Predictive Maintenance',
    keywords='Arimo Predictive Maintenance',
    namespace_packages=['arimo'],
    packages=find_namespace_packages(include=['arimo.*']),
    include_package_data=True,
    install_requires=
        [s for s in
            {i.strip()
             for i in open('requirements.txt').readlines()}
         if not (s.startswith('#') or s.startswith('http'))],
    scripts=['bin/arimo-pm'])
