#!/usr/bin/python

__author__ = 'Ryan McGrath <ryan@venodesigns.net>'
__version__ = '0.7'

# For the love of god, use Pip to install this.

# Distutils version
METADATA = dict(
	name = "tango",
	version = __version__,
	py_modules = ['tango/tango'],
	author='Ryan McGrath',
	author_email='ryan@venodesigns.net',
	description='A new and easy way to access Twitter data with Python.',
	license='MIT License',
	url='http://github.com/ryanmcgrath/tango/tree/master',
	keywords='twitter search api tweet tango',
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
