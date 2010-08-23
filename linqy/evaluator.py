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
	def __init__(self, source, enum=False):
		if isinstance(source, basestring):
			self.source = compile(source, '<string>', 'eval')
			self.is_code = True
		else:
			self.source = source
			self.is_code = False
		self.index = 0
		self.enum = enum
	
	def __call__(self, *args):
		if self.source is None:
			if len(args) == 1:
				return args[0]
			else:
				return tuple(*args)

		if self.enum:
			args = (self.index,) + args
			self.index += 1

		if self.is_code:
			# setup local envs
			for i, arg in enumerate(args):
				for name in __fieldnames__[i]:
					locals().__setitem__(name, arg)
			return eval(self.source)

		# function
		return self.source(*args)

