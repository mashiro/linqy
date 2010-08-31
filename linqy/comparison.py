#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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
	
class Not(ComparisonWrapper):
	def __cmp__(self, other):
		return -self.defaultcmp(other)

