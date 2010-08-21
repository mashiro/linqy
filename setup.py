#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import linqy

setup(
	name = 'linqy',
	version = linqy.__version__,
	description = 'LINQ like library for Python',
	license = linqy.__license__,
	author = linqy.__author__,
	author_email = linqy.__email__,
	url = linqy.__url__,
	keywords = 'linq library',
	packages = find_packages(),
	zip_safe = True,
	)

