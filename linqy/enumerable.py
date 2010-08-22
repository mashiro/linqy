#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import functools
import itertools
from linqy.evaluator import Evaluator
from linqy.utils import *

# decorators
#--------------------------------------------------------------------------------
def linqmethod(func):
	@functools.wraps(func)
	def outer(*args, **kwargs):
		def inner(enumerable):
			return getattr(enumerable, func.__name__)(*args, **kwargs)
		return inner
	globals().__setitem__(func.__name__, outer)
	return func

#def lazymethod(func):
#	@functools.wraps(func)
#	def inner(*args, **kwargs):
#		return Enumerable(lambda: func(*args, **kwargs))
#	return inner

# generator
#--------------------------------------------------------------------------------
#def make(iterable, *methods):
#	def inner():
#		for item in iterable:
#			yield item
#	return Enumerable(lambda: inner()).combine(*methods)
#
#def empty():
#	return make([])
#
#@lazymethod
#def range(*args):
#	s = slice(*args)
#	return iter(linqy.utils.xrange(s.start or 0, s.stop or sys.maxsize, s.step or 1))
#
#@lazymethod
#def countup(start=0, step=1):
#	n = start
#	while True:
#		yield n
#		n += step
#
#@lazymethod
#def cycle(iterable):
#	return itertools.cycle(iterable)
#
#@lazymethod
#def repeat(item, count=None):
#	if count is None:
#		while True:
#			yield item
#	else:
#		for i in range(count):
#			yield item
#
#@lazymethod
#def generate(generator, count=None):
#	generator = Evaluator(generator)
#	if count is None:
#		while True:
#			yield generator()
#	else:
#		for i in range(count):
#			yield generator()
#
## functions
##--------------------------------------------------------------------------------
#@lazymethod
#def iselect(iterable, selector=None):
#	evaluator = Evaluator(selector)
#	for item in iterable:
#		yield evaluator(item)
#
#@lazymethod
#def iselectmany(iterable, selector=None):
#	for it in iselect(iterable, selector):
#		for item in it:
#			yield item
#
#@lazymethod
#def iwhere(iterable, pred=bool):
#	return linqy.utils.ifilter(Evaluator(pred), iterable)
#
#@lazymethod
#def itake(iterable, count):
#	return itertools.islice(iterable, count)
#
#@lazymethod
#def itakewhile(iterable, pred=bool):
#	return itertools.takewhile(Evaluator(pred), iterable)
#
#@lazymethod
#def iskip(iterable, count):
#	return itertools.islice(iterable, count, None)
#
#@lazymethod
#def iskipwhile(iterable, pred=bool):
#	return itertools.dropwhile(Evaluator(pred), iterable)
#
#@lazymethod
#def izip(*iterables):
#	return linqy.utils.izip(*iterables)
#
#@lazymethod
#def iconcat(*iterables):
#	return itertools.chain(*iterables)
#
#@lazymethod
#def iorderby(iterable, key=None):
#	if key is None:
#		return iter(sorted(iterable, key=None))
#	else:
#		return iter(sorted(iterable, key=Evaluator(key)))
#
#@lazymethod
#def ireverse(iterable):
#	return reversed(list(iterable))
#
#@lazymethod
#def idistinct(iterable, key=None):
#	evaluator = Evaluator(key)
#	s = set()
#	for item in iterable:
#		h = hash(evaluator(item))
#		if h not in s:
#			s.add(h)
#			yield item
#
#def iall(iterable, pred=bool):
#	for item in linqy.utils.ifilterfalse(Evaluator(pred), iterable):
#		return False
#	return True
#
#def iany(iterable, pred=bool):
#	for item in linqy.utils.ifilter(Evaluator(pred), iterable):
#		return True
#	return False
#
#def ielementat(iterable, index):
#	try:
#		return linqy.utils.next(itertools.islice(iterable, index, index+1))
#	except StopIteration:
#		raise IndexError
#
#def inth(iterable, index):
#	return ielementat(iterable, index)
#
#def ifirst(iterable, pred=None):
#	evaluator = Evaluator(pred)
#	it = iter(iterable)
#	try:
#		while True:
#			item = linqy.utils.next(it)
#			if pred is None or evaluator(item):
#				return item
#	except StopIteration:
#		raise IndexError
#
#def ilast(iterable, pred=None):
#	return ifirst(ireverse(iterable), pred)
#
#def ido(iterable, func):
#	evaluator = Evaluator(func)
#	for item in iterable:
#		evaluator(item)
#		yield item
#
#def iforeach(iterable, func):
#	evaluator = Evaluator(func)
#	for item in iterable:
#		evaluator(item)


class Enumerable(object):
	def __init__(self, func):
		self._func = func
	
	def __iter__(self):
		return self._func()

	@linqmethod
	def combine(self, *methods):
		e = self
		for method in methods:
			e = method(e)
		return e

	# equality
	#--------------------------------------------------------------------------------
	@linqmethod
	def sequence_equal(self, second, selector=None):
		return iequal(self, second, selector)

	# projection
	#--------------------------------------------------------------------------------
	@linqmethod
	def select(self, selector):
		def inner():
			return imap(Evaluator(selector), self)
		return Enumerable(lambda: inner())

	@linqmethod
	def selectmany(self, selector):
		def inner():
			return itertools.chain(*self.select(selector))
		return Enumerable(lambda: inner())

	# filtering
	#--------------------------------------------------------------------------------
	@linqmethod
	def where(self, pred):
		def inner():
			return ifilter(Evaluator(pred), self)
		return Enumerable(lambda: inner())

	@linqmethod
	def oftype(self, type):
		def inner():
			return ifilter(lambda x: isinstance(x, type), self)
		return Enumerable(lambda: inner())

	# partitioning
	#--------------------------------------------------------------------------------
	@linqmethod
	def skip(self, count):
		def inner():
			return itertools.islice(self, count, None)
		return Enumerable(lambda: inner())

	@linqmethod
	def skipwhile(self, pred):
		def inner():
			return itertools.dropwhile(Evaluator(pred), self)
		return Enumerable(lambda: inner())

	@linqmethod
	def take(self, count):
		def inner():
			return itertools.islice(self, count)
		return Enumerable(lambda: inner())

	@linqmethod
	def takewhile(self, pred):
		def inner():
			return itertools.takewhile(Evaluator(pred), self)
		return Enumerable(lambda: inner())


# equality
#--------------------------------------------------------------------------------
def iequal(first, second, selector=None):
	f = Evaluator(selector)
	items1 = list(first)
	items2 = list(second)
	if len(items1) != len(items2):
		return False
	for i in xrange(len(items1)):
		item1 = items1[i]
		item2 = items2[i]
		if selector is None:
			if item1 != item2:
				return False
		else:
			if f(item1) != f(item2):
				return False
	return True

# generation
#--------------------------------------------------------------------------------
def make(iterable):
	def inner():
		for item in iterable:
			yield item
	return Enumerable(lambda: inner())

def empty():
	return make([])

def range(*args):
	def inner():
		s = slice(*args)
		return iter(xrange(s.start or 0, s.stop or sys.maxsize, s.step or 1))
	return Enumerable(lambda: inner())

def repeat(item, count=None):
	def inner():
		if count is None:
			while True:
				yield item
		else:
			for i in range(count):
				yield item
	return Enumerable(lambda: inner())

def cycle(iterable):
	def inner():
		saved = [item for item in iterable]
		while saved:
			for item in saved:
				yield item
	return Enumerable(lambda: inner())

def countup(start=0, step=1):
	def inner():
		n = start
		while True:
			yield n
			n += step
	return Enumerable(lambda: inner())

