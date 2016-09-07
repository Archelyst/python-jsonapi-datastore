#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("jsonapi_datastore.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='jsonapi-datastore',
    version=__version__,
    description=('A lightweight library handling structured JSONAPI responses.'),
    long_description=read('README.md'),
    author='Tim-Christian Mundt',
    author_email='dev@tim-erwin.de',
    url='https://github.com/Tim-Erwin/python-jsonapi-datastore',
    py_modules=['jsonapi_datastore'],
    zip_safe=False,
    keywords=('JSONAPI', 'JSON', 'API'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
