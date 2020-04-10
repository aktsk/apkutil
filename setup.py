#!/usr/bin/env python3
# coding: UTF-8

from setuptools import setup

setup(
    name="apkpatch",
    version="0.0.1",
    description="unpacking, patch, packing script",
    author="Taichi Kotake",
    packages=['apkpatch'],
    entry_points={
        'console_scripts':[
            'apkpatch = apkpatch.cli:main',
        ],
    },
    install_requires=[
        'colorama',
    ],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
