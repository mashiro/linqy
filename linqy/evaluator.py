#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class Evaluator(object):
	def __init__(self, source):
		if isinstance(source, basestring):
			self.source = compile(source, '<string>', 'eval')
			self.is_code = True
		else:
			self.source = source
			self.is_code = False
	
	def __call__(self, *args):
		if self.is_code:
			names = [['item1', 'first', 'item'],
					 ['item2', 'second'],
					 ['item3', 'third'],
					 ['item4', 'fourth'],
					 ['item5', 'fifth']]
			for i, arg in enumerate(args):
				for name in names[i]:
					locals().__setitem__(name, arg)
			return eval(self.source)
		else:
			return self.source(*args)

