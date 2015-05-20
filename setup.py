#!/usr/bin/env python
from setuptools import setup, find_packages
# import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.md')).read()

version = '0.2'

install_requires = [
    'click',
    'CoffeeScript',
    'PyYAML',
    'sh'
]


setup(name='fixxd',
      version=version,
      description="iOS UIAutomation tests launcher",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      ],
      keywords='ios, uiautomation, tests, instruments, ui, automation',
      author='Francescu',
      author_email='',
      url='https://github.com/Stupeflix/fixxd',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts':
          ['fixxd=fixxd.core:fixxd']
      }
      )
