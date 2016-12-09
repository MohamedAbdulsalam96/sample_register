# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '3.5.1'

setup(
    name='sample_register',
    version=version,
    description='Detail Information of collected samples.',
    author='indictrans',
    author_email='tejal.s@indictranstech.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
