#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import inspect
import types

class Function(object):
	def __init__(self, func):
		self.index = 0
		if func:
			self.func = func
			self.spec = inspect.getargspec(func)
			self.arity = len(self.spec[0])
			if type(func) is types.MethodType:
				self.arity -= 1 # remove self or cls
		else:
			self.func = None
			self.spec = None
			self.arity = None

	def __bool__(self):
		return self.func is not None
	
	def __nonzero__(self):
		return self.__bool__()
	
	def __call__(self, *args, **kwargs):
		try:
			if self.func:
				if args:
					args += (self.index,)
				return self.func(*args[:self.arity], **kwargs)
			else:
				if args:
					return args[0]
				else:
					return args
		finally:
			self.index += 1

