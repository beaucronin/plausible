# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use Python Boilerplate to start
# simple, usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os

from setuptools import setup, find_packages

# Meta information
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
    
setup(
    # Basic info
    name='python-plausible',
    version=version,
    author='Beau Cronin',
    author_email='beau.cronin@gmail.com',
    url='https://github.com/beaucronin/plausible',
    description='Python client for plausible serverless',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    # Packages and depencies
    # package_dir={'': 'src'},
    # packages=find_packages('src'),
    install_requires=[
    ],

    # Scripts
    # entry_points={
    #     'console_scripts': [
    #         'python-boilerplate = python_boilerplate.__main__:main'],
    # },

    # Other configurations
    zip_safe=False,
    platforms='any',
)