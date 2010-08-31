#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import functools
import itertools
from linqy.function import Function
from linqy.comparison import Not
from linqy.utils import *

class Enumerable(object):
	''' enumerable object '''

	def __init__(self, generator):
		self._generator = generator
	
	def __iter__(self):
		return self._generator()

class OrderedEnumerable(Enumerable):
	def __init__(self, iterable, key, reverse, parent=None):
		self._iterable = iterable
		self._key = key
		self._reverse = reverse
		self._parent = parent
	
	def __iter__(self):
		return iter(sorted(self._iterable, key=self._key, reverse=self._reverse))

	def contexts(self):
		results = []
		parent = self._parent
		while parent is not None:
			results.append(parent)
			parent = parent._parent
		return results

def linqmethod(type):
	def outer(func):
		@functools.wraps(func)
		def method(self, *args, **kwargs):
			return func(self, *args, **kwargs)
		setattr(type, func.__name__, method)
		return func
	return outer

def lazymethod(type):
	def outer(func):
		@functools.wraps(func)
		def inner(*args, **kwargs):
			return type(lambda: func(*args, **kwargs))
		return inner
	return outer


# generation
#--------------------------------------------------------------------------------
def make(iterable):
	return asenumerable(iterable)

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


# conversions
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
def asenumerable(iterable):
	if isinstance(iterable, Enumerable):
		return iterable
	else:
		return Enumerable(lambda: iter(iterable))

@linqmethod(Enumerable)
def tolist(iterable):
	return list(iterable)


# projection
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
@lazymethod(Enumerable)
def select(iterable, selector):
	return imap(Function(selector), iterable)

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def selectmany(iterable, selector, result=None):
	selector = Function(selector)
	result = Function(result)
	for x in make(iterable):
		for y in selector(x):
			if result:
				yield result(x, y)
			else:
				yield y

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def zip(iterable, *iterables):
	return izip(iterable, *iterables)

@linqmethod(Enumerable)
def enumerate(iterable):
	return countup().zip(iterable)


# filtering
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
@lazymethod(Enumerable)
def where(iterable, pred):
	return ifilter(Function(pred), iterable)

@linqmethod(Enumerable)
def oftype(iterable, type):
	return where(iterable, lambda x: isinstance(x, type))


# ordering
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
def orderby(iterable, key=None, reverse=False):
	return OrderedEnumerable(iterable, key, reverse)
#def orderby(iterable, key=None, reverse=False):
#	return iter(sorted(iterable, key=key, reverse=reverse))

@linqmethod(OrderedEnumerable)
def thenby(ordered, key=None, reverse=False):
	return OrderedEnumerable(ordered._iterable, key, reverse, ordered)

# thenby does'nt implement it
#
# if you want this.
#
# items.OrderBy(item => item.first)
#      .ThenByDescending(item => item.second);
#
# it likes
#
# items.orderby(key=lambda item: (item.first, -item.second))

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def reverse(iterable):
	return reversed(list(iterable))


# partitioning
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
@lazymethod(Enumerable)
def skip(iterable, count):
	return itertools.islice(iterable, count, None)

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def skipwhile(iterable, pred):
	return itertools.dropwhile(Function(pred), iterable)

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def take(iterable, count):
	return itertools.islice(iterable, count)

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def takewhile(iterable, pred):
	return itertools.takewhile(Function(pred), iterable)


# equality
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
def sequenceequal(first, second, selector=None):
	selector = Function(selector)
	first, second = imap(list, [first, second])
	if len(first) != len(second):
		return False
	for a, b in izip(first, second):
		if selector(a) != selector(b):
			return False
	return True


# action
#--------------------------------------------------------------------------------
@linqmethod(Enumerable)
def foreach(iterable, action):
	action = Function(action)
	for item in iterable:
		action(item)

@linqmethod(Enumerable)
@lazymethod(Enumerable)
def do(iterable, action):
	action = Function(action)
	for item in iterable:
		action(item)
		yield item

