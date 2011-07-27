#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from linqy import meta

setup(name='linqy',
      version=meta.__version__,
      description=meta.__doc__,
      author=meta.__author__,
      author_email=meta.__email__,
      url=meta.__url__,
      license=meta.__license__,
      packages=['linqy'],
      keywords=['LINQ', 'Enumerable', 'Iterable', 'Library'],
      test_suite='tests.suite')
