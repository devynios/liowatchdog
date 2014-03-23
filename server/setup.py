#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='lio_watchdog',
    version='0.0.1',
    packages=['lio_watchdog'],
    package_data={'lio_watchdog': ['templates/*']},
    scripts=['lio-watchdog.py'],
    description='lio watchdog',
    install_requires=[
        "Flask",
    ],
)
