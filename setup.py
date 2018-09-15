#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Tunisia Pension specific model for OpenFisca -- a versatile microsimulation free software"""


from setuptools import setup, find_packages


classifiers = """\
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
"""

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-Tunisia-Pension',
    version = '0.9.2',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'benefit microsimulation pension social tax tunisia',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-tunisia-pension',

    data_files = [],
    extras_require = dict(
        tests = [
            'nose',
            ],
        ),
    install_requires = [
        'Babel >= 0.9.4',
        "Bottleneck >= 1.2.0",
        'Biryani[datetimeconv] >= 0.10.4',
        'OpenFisca-Core >= 24.0, < 25.0',
        'PyYAML >= 3.10',
        'scipy >= 0.12',
        ],
    packages = find_packages(exclude=['openfisca_tunisia_pension.tests*']),
    )
