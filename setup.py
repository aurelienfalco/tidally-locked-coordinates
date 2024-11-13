#!/usr/bin/env python
from setuptools import find_packages

from numpy.distutils.core import setup, Extension
from numpy.distutils import log
import os
import glob

packages = find_packages(exclude=('tests', 'doc'))
provides = ['TL_coordinates', ]

requires = []

install_requires = ['numpy',
                    'scipy',
                    'netCDF4',
]

classifiers = [
    'Development Status :: 2 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries',
    'Topic :: Scientific/Engineering :: Astronomy',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
]

# Handle versioning
version = '1.0.1-alpha'

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='TL_coordinates',
      author='Aurélien Falco',
      author_email='aurelien.falco@gmail.com',
      license="BSD",
      version=version,
      description='TL coordinates',
      classifiers=classifiers,
      packages=packages,
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords = ['exoplanet','simulation','atmosphere','atmospheric'],
      include_package_data=True,
      provides=provides,
      requires=requires,
      setup_requires=["numpy"],
      install_requires=install_requires,
      extras_require={
        'Plot':  ["matplotlib"], },
      )
