#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from linqy.utils import findattr

basestring = findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

__fieldnames__ = [
	['item1', 'first', 'item'],
	['item2', 'second'],
	['item3'],
	['item4'],
	['item5'],
	['item6'],
	['item7'],
	['item8'],
	['item9']
]

class Evaluator(object):
	def __init__(self, source):
		if isinstance(source, basestring):
			self.source = compile(source, '<string>', 'eval')
			self.is_code = True
		else:
			self.source = source
			self.is_code = False
	
	def __call__(self, *args):
		if self.source is None:
			if len(args) == 1:
				return args[0]
			else:
				return tuple(*args)

		if self.is_code:
			# setup local envs
			for i, arg in enumerate(args):
				for name in __fieldnames__[i]:
					locals().__setitem__(name, arg)
			return eval(self.source)

		# function
		return self.source(*args)

