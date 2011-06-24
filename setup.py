#!/usr/bin/env python
from distutils.core import setup

setup(name='firehub',
      version='0',
      description='Github notification broker',
      url='https://github.com/lvh/firehub',

      author='Laurens Van Houtven',
      author_email='_@lvh.cc',

      packages=['firehub'],

      requires=['twisted'],

      license='ISC',
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Twisted",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email :: Post-Office",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Version Control",
        ])
