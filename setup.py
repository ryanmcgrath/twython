#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

__author__ = 'Ryan McGrath <ryan@venodesigns.net>'
__version__ = '2.0.0'

setup(
    # Basic package information.
    name='twython',
    version=__version__,
    packages=find_packages(),

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['simplejson', 'oauth2', 'requests'],

    # Metadata for PyPI.
    author='Ryan McGrath',
    author_email='ryan@venodesigns.net',
    license='MIT License',
    url='http://github.com/ryanmcgrath/twython/tree/master',
    keywords='twitter search api tweet twython',
    description='An easy (and up to date) way to access Twitter data with Python.',
    long_description=open('README.markdown').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet'
    ]
)
