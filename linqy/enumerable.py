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

def lazymethod(type):
	def outer(func):
		@functools.wraps(func)
		def inner(*args, **kwargs):
			if isinstance(type, basestring):
				newtype = globals().__getitem__(type)
			else:
				newtype = type
			return newtype(lambda: func(*args, **kwargs))
		return inner
	return outer

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
		return reduce(lambda e, m: m(e), methods, self)

	# equality
	#--------------------------------------------------------------------------------
	@linqmethod
	def sequence_equal(self, second, selector=None):
		return iequal(self, second, selector)

	# projection
	#--------------------------------------------------------------------------------
	@linqmethod
	@lazymethod('Enumerable')
	def select(self, selector, enum=False):
		return imap(Evaluator(selector, enum=enum), self)

	@linqmethod
	@lazymethod('Enumerable')
	def selectmany(self, selector, result=None, enum=False):
		if result is not None:
			result = Evaluator(result)
		for it in self.select(selector, enum=enum):
			for item in it:
				if result is not None:
					yield result(it, item)
				else:
					yield item
	
	@linqmethod
	@lazymethod('Enumerable')
	def zip(self, *iterables):
		return izip(self, *iterables)

	@linqmethod
	def enumerate(self):
		return countup().zip(self)

	# filtering
	#--------------------------------------------------------------------------------
	@linqmethod
	@lazymethod('Enumerable')
	def where(self, pred, enum=False):
		return ifilter(Evaluator(pred, enum=enum), self)

	@linqmethod
	def oftype(self, type):
		return self.where(lambda x: isinstance(x, type))

	# partitioning
	#--------------------------------------------------------------------------------
	@linqmethod
	@lazymethod('Enumerable')
	def skip(self, count):
		return itertools.islice(self, count, None)

	@linqmethod
	@lazymethod('Enumerable')
	def skipwhile(self, pred, enum=False):
		return itertools.dropwhile(Evaluator(pred, enum=enum), self)

	@linqmethod
	@lazymethod('Enumerable')
	def take(self, count):
		return itertools.islice(self, count)

	@linqmethod
	@lazymethod('Enumerable')
	def takewhile(self, pred, enum=False):
		return itertools.takewhile(Evaluator(pred, enum=enum), self)



# equality
#--------------------------------------------------------------------------------
def iequal(first, second, selector=None):
	func = Evaluator(selector)
	items1 = list(first)
	items2 = list(second)
	if len(items1) != len(items2):
		return False
	for i in irange(len(items1)):
		item1 = items1[i]
		item2 = items2[i]
		if selector is None:
			if item1 != item2:
				return False
		else:
			if func(item1) != func(item2):
				return False
	return True

# generation
#--------------------------------------------------------------------------------
def make(iterable, *methods):
	return Enumerable(lambda: iter(iterable)).combine(*methods)

def empty():
	return make([])

@lazymethod(Enumerable)
def range(*args):
	s = slice(*args)
	return iter(irange(s.start or 0, s.stop or sys.maxsize, s.step or 1))

@lazymethod(Enumerable)
def repeat(item, count=None):
	if count is None:
		while True:
			yield item
	else:
		for i in irange(count):
			yield item

@lazymethod(Enumerable)
def cycle(iterable):
	return itertools.cycle(iterable)

@lazymethod(Enumerable)
def countup(start=0, step=1):
	n = start
	while True:
		yield n
		n += step

