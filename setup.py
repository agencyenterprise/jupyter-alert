# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='jupyter_alert',
    version='0.1.0',
    description='A Jupyter magic to alert execution completion',
    author='Diogo de Lucena, AE Studio',
    author_email='diogo@ae.studio',
    url='https://github.com/agencyenterprise/jupyter-alert',
    license='BSD-3-Clause',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'ipython',
        'jupyter'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ]
)
