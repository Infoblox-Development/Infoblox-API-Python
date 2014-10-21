import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='infoblox',
    version='1.1',
    description='The module implements Infoblox IPAM API via REST API',
    long_description=README,
    license = 'Licensed under the Apache License, Version 2.0',
    packages=['.'],
    install_requires=['requests'],
)
