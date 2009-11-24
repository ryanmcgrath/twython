#!/usr/bin/python

import sys, os

__author__ = 'Ryan McGrath <ryan@venodesigns.net>'
__version__ = '0.9'

# For the love of god, use Pip to install this.

# Distutils version
METADATA = dict(
	name = "twython",
	version = __version__,
	py_modules = ['twython'],
	author = 'Ryan McGrath',
	author_email = 'ryan@venodesigns.net',
	description = 'An easy (and up to date) way to access Twitter data with Python.',
	long_description = open("README.markdown").read(),
	license = 'MIT License',
	url = 'http://github.com/ryanmcgrath/twython/tree/master',
	keywords = 'twitter search api tweet twython',
)

# Setuptools version
SETUPTOOLS_METADATA = dict(
	install_requires = ['setuptools', 'simplejson'],
	include_package_data = True,
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Communications :: Chat',
		'Topic :: Internet',
	]
)

def Main():
	try:
		import setuptools
		METADATA.update(SETUPTOOLS_METADATA)
		setuptools.setup(**METADATA)
	except ImportError:
		import distutils.core
		distutils.core.setup(**METADATA)

if __name__ == '__main__':
  Main()
