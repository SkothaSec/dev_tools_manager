#!/usr/bin/env python3
from setuptools import setup

setup(
   name = 'skothaws',
    version = '0.1',
    py_modules = ['aws_config_setup'],
    install_requires = [
        'Click',
    ],
    entry_points = '''
[console_scripts]
skothaws = aws_config_setup:cli
    ''',
)
