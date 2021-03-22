from setuptools import find_namespace_packages, setup


setup(
    name='H1st-PredMaint',
    author='h1st LLC',
    author_email='Info@H1st.ai',
    url='https://GitHub.com/H1st-AI/PredMaint',
    version='0.0.0',
    description='H1st Predictive Maintenance',
    long_description='H1st Predictive Maintenance',
    keywords='H1st Predictive Maintenance',
    namespace_packages=['h1st'],
    packages=find_namespace_packages(include=['h1st.*']),
    include_package_data=True,
    install_requires=[s for s in
                      {i.strip()
                       for i in open('requirements.txt').readlines()}
                      if not (s.startswith('#') or s.startswith('http'))],
    scripts=['bin/h1st-pm'])
