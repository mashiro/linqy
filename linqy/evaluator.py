#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from linqy.utils import basestring

__fieldnames__ = [
	['_1', '_'],
	['_2'],
	['_3'],
	['_4'],
	['_5']
]

class Evaluator(object):
	def __init__(self, func, enum=False):
		self.is_str = isinstance(func, basestring)
		self.func = func
		self.enum = enum
		self.index = 0
		self.source = func if self.is_str else None
		self.compiled = not self.is_str
	
	def __nonzero__(self):
		return self.func is not None

	def __bool__(self):
		return self.__nonzero__()
	
	def __call__(self, *args):
		if not self:
			if len(args) == 1:
				return args[0]
			else:
				return tuple(*args)

		if self.enum:
			# append index
			args = args + (self.index,)
			self.index += 1

		if self.is_str:
			# compile on first time.
			if not self.compiled:
				self.func = compile(self.source, '<string>', 'eval')
				self.compiled = True

			# setup local envs
			for i, arg in enumerate(args):
				for name in __fieldnames__[i]:
					locals().__setitem__(name, arg)
			return eval(self.func)
		else:
			# call function
			return self.func(*args)

