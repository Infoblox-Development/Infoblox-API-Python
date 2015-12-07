#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from pip.download import PipSession
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()


def get_requirements(filepath):
    analysis = parse_requirements(filepath, session=PipSession())
    return [str(requirement.req) for requirement in analysis]

requirements = get_requirements('requirements.txt')
test_requirements = get_requirements('testing_requirements.txt')


setup(
    name='infoblox',
    version='1.1.1',
    description='The module implements Infoblox IPAM API via REST API.',
    long_description=readme + '\n\n' + changelog,
    author="Equifax CIA",
    author_email='cia@equifax.com',
    url='https://github.com/EFXCIA/Infoblox-API-Python',
    packages=[
        'infoblox',
    ],
    package_dir={'infoblox':
                 'infoblox'},
    entry_points={
        'console_scripts': [
            'infoblox = infoblox.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License, Version 2.0",
    keywords='infoblox',
    classifiers=[
        # 'Development Status :: 1 - Planning'
        'Development Status :: 2 - Pre-Alpha'
        # 'Development Status :: 3 - Alpha'
        # 'Development Status :: 4 - Beta'
        # 'Development Status :: 5 - Production/Stable'
        # 'Development Status :: 6 - Mature'
        # 'Development Status :: 7 - Inactive'
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
