#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import itertools

class AttributeNotFoundError(Exception):
	pass

def findattr(*candidates):
	for candidate in candidates:
		if isinstance(candidate, tuple):
			module, name = candidate
			if isinstance(module, dict):
				if name in module:
					return module[name]
			else:
				if hasattr(module, name):
					return getattr(module, name)
		else:
			return candidate
	raise AttributeNotFoundError

imap = findattr((itertools, 'imap'), (__builtins__, 'map'))
ifilter = findattr((itertools, 'ifilter'), (__builtins__, 'filter'))
ifilterfalse = findattr((itertools, 'ifilterfalse'), (itertools, 'filterfalse'))
next = findattr((__builtins__, 'next'), lambda x: x.next())
xrange = findattr((__builtins__, 'xrange'), range)
basestring = findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

