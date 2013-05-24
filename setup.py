#!/usr/bin/env python

import os
import sys

from setuptools import setup

__author__ = 'Ryan McGrath <ryan@venodesigns.net>'
__version__ = '2.10.1'

packages = [
    'twython',
    'twython.streaming'
]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    # Basic package information.
    name='twython',
    version=__version__,
    packages=packages,

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['requests==1.2.2', 'requests_oauthlib==0.3.2'],

    # Metadata for PyPI.
    author='Ryan McGrath',
    author_email='ryan@venodesigns.net',
    license='MIT License',
    url='http://github.com/ryanmcgrath/twython/tree/master',
    keywords='twitter search api tweet twython stream',
    description='Actively maintained, pure Python wrapper for the Twitter API. Supports both normal and streaming Twitter APIs',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet'
    ]
)
