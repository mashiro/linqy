#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from linqy.utils import findattr

# env {{{1
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

# hack {{{1
basestring = findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

class Evaluator(object): # {{{1
	def __init__(self, source):
		if isinstance(source, basestring):
			self.source = compile(source, '<string>', 'eval')
			self.is_code = True
		else:
			self.source = source
			self.is_code = False
	
	def __call__(self, *args):
		if self.is_code:
			for i, arg in enumerate(args):
				for name in __fieldnames__[i]:
					locals().__setitem__(name, arg)
			return eval(self.source)
		else:
			return self.source(*args)

