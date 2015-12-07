#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools config file
"""

import sys
import pip
from pip.req import parse_requirements
from setuptools import setup, find_packages
import os
from uberpong import __version__ as version
from uberpong import __author__ as author
from uberpong import PKG_URL as pkg_url
from uberpong import __name__ as pkg_name


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=pip.download.PipSession())

# this is the way assets are distributed
sys_prefix = os.path.join(sys.prefix, "share/{}".format(pkg_name))
datadir = 'assets'
data_files = [ (os.path.join(sys_prefix, d), [os.path.join(d, f) for f in files]) for d,folders,files in os.walk(datadir)]

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

# description
desc = "An Uber-engineered PONG clone"

setup(
    name=pkg_name,
    version=version,
    packages=find_packages(),
    author=author,
    author_email="alejandroricoveri@gmail.com",
    description=desc,
    long_description=open('README.md').read(),
    url=pkg_url,
    license='MIT',
    download_url="{url}/tarball/{version}".format(url=pkg_url, version=version),
    keywords=['games', 'pong'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Games/Entertainment :: Arcade',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
    ],
    data_files=data_files, # assets
    entry_points={
        'gui_scripts': [
            'uberpong = uberpong.__main__:main',
        ],
    },
    install_requires = reqs,
)
