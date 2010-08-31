#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import itertools
import functools

def anonymouse(**kwargs):
	''' make anonymouse type instance '''
	return type('', (object,), kwargs)()


class ComparisonWrapper(object):
	def __init__(self, wrapped):
		self.wrapped = wrapped
	
	def __cmp__(self, other):
		return self.defaultcmp(other)

	def defaultcmp(self, other):
		return cmp(self.wrapped, self.wrappedvalue(other))
	
	@classmethod
	def wrappedvalue(cls, value):
		if isinstance(value, ComparisonWrapper):
			return value.wrapped
		return value
	
class Negate(ComparisonWrapper):
	def __cmp__(self, other):
		return -self.defaultcmp(other)


class AttributeNotFoundError(Exception):
	pass

def findattr(*candidates):
	''' find a attribute in module or dict '''
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
izip = findattr((itertools, 'izip'), (__builtins__, 'zip'))
ifilter = findattr((itertools, 'ifilter'), (__builtins__, 'filter'))
ifilterfalse = findattr((itertools, 'ifilterfalse'), (itertools, 'filterfalse'))
irange = findattr((__builtins__, 'xrange'), range)
next = findattr((__builtins__, 'next'), lambda x: x.next())
reduce = findattr((__builtins__, 'reduce'), (functools, 'reduce'))
basestring = findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

