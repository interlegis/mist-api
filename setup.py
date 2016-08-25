# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
        name='mist_api',
        version='0.1',
        description='Python API for access MistServer REST stats',
        author='Edward Ribeiro',
        author_email='eribeiro@interlegis.leg.br',
        url='https://github.com/interlegis/mist-api.git',
        packages=find_packages(exclude=('tests', 'docs'))
)
