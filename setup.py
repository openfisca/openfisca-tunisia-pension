#! /usr/bin/env python


'''Tunisia Pension specific model for OpenFisca -- a versatile microsimulation free software'''


from setuptools import setup, find_packages


classifiers = '''\
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
'''

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-Tunisia-Pension',
    version = '2.0.0',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.org',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'benefit microsimulation pension social tax tunisia',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-tunisia-pension',

    data_files = [],
    extras_require = {
        'dev': [
            'autopep8 >=2.0.2, <3.0',
            'flake8 >=6.0.0, <7.0.0',
            'flake8-print >=5.0.0, <6.0.0',
            'flake8-quotes >=3.3.2',
            'pytest >=7.2.2, <8.0',
            'scipy >=1.10.1, <2.0',  # Only used to test de_net_a_brut reform
            'requests >=2.28.2, <3.0',
            'yamllint >=1.30.0, <2.0'
            ],
        },
    install_requires = [
        'bottleneck >=1.3.2,<=2.0.0',
        'OpenFisca-Core >= 41.4.1, < 42.0',
        'scipy >= 0.12',
        'OpenFisca-Tunisia >= 0.20, < 0.21',
        ],
    packages = find_packages(exclude=['openfisca_tunisia_pension.tests*']),
    )
