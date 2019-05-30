#!/usr/bin/env python3

"""
Setup.py
This module is used for installation of this code directly on the machine
"""

import os.path

from setuptools import setup, find_packages

PACKAGE_NAME = "conjur-iam-client"
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(CURRENT_DIR, PACKAGE_NAME, "version.py")

VERSION_DATA = {}
with open(VERSION_FILE, 'r') as version_fp:
    exec(version_fp.read(), VERSION_DATA)

long_description=""
with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name="conjur-iam-client",
    version=VERSION_DATA['__version__'],
    python_requires='>=3.5',
    packages=find_packages(exclude=("test")),
    zip_safe=True,

    package_data={
        '': ['*.md'],
    },

    author="Andrew Copeland",
    description="Using the Conjur SDK with iam roles",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache 2.0",
    url="https://github.com/AndrewCopeland/conjur-iam-api-key3",
    keywords=[
        "conjur",
        "cyberark",
        "microservices"
        "privileged access",
        "security",
        "vault",
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Office/Business",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        "Topic :: Utilities",
    ],
)
