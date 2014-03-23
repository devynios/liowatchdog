#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name='lio_watchdog',
    version='0.0.1',
    packages=['lio_watchdog'],
    package_data={'lio_watchdog': ['templates/*']},
    description='lio watchdog',
    install_requires=[
        'Flask',
    ],
    entry_points={
        'console_scripts': [
            'lio_watchdog_server = lio_watchdog:run',
        ],
    },
)
