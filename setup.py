#!/usr/bin/env python3
from setuptools import setup
from escleaner import __version__

setup(name='escleaner',
      version=__version__,
      description='Utility for deleteding logstash-elasticearch indices by age',
      url='http://gitlab.davepedu.com/dave/escleaner',
      author='dpedu',
      author_email='dave@davepedu.com',
      packages=['escleaner'],
      entry_points={
          'console_scripts': [
              'escleaner = escleaner.escleaner:shell',
          ]
      },
      install_requires=[
          'requests==2.10.0',
      ],
      zip_safe=False)
