#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import functools
import itertools
from linqy.function import Function
from linqy.utils import *

class Enumerable(object):
	''' enumerable object '''

	def __init__(self, generator):
		self._generator = generator
	
	def __iter__(self):
		return self._generator()

	def tolist(self):
		return list(self)


def linqmethod(func):
	@functools.wraps(func)
	def method(self, *args, **kwargs):
		return func(self, *args, **kwargs)
	setattr(Enumerable, func.__name__, method)
	return func

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
@linqmethod
def asenumerable(iterable):
	if isinstance(iterable, Enumerable):
		return iterable
	else:
		return Enumerable(lambda: iter(iterable))


# projection
#--------------------------------------------------------------------------------
@linqmethod
@lazymethod(Enumerable)
def select(iterable, selector):
	return imap(Function(selector), iterable)

@linqmethod
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

@linqmethod
@lazymethod(Enumerable)
def zip(iterable, *iterables):
	return izip(iterable, *iterables)

@linqmethod
def enumerate(iterable):
	return countup().zip(iterable)


# filtering
#--------------------------------------------------------------------------------
@linqmethod
@lazymethod(Enumerable)
def where(iterable, pred):
	return ifilter(Function(pred), iterable)

@linqmethod
def oftype(iterable, type):
	return where(iterable, lambda x: isinstance(x, type))


# partitioning
#--------------------------------------------------------------------------------
@linqmethod
@lazymethod(Enumerable)
def skip(iterable, count):
	return itertools.islice(iterable, count, None)

@linqmethod
@lazymethod(Enumerable)
def skipwhile(iterable, pred):
	return itertools.dropwhile(Function(pred), iterable)

@linqmethod
@lazymethod(Enumerable)
def take(iterable, count):
	return itertools.islice(iterable, count)

@linqmethod
@lazymethod(Enumerable)
def takewhile(iterable, pred):
	return itertools.takewhile(Function(pred), iterable)


# equality
#--------------------------------------------------------------------------------
@linqmethod
def sequenceequal(first, second, selector=None):
	selector = Function(selector)
	first = list(first)
	second = list(second)
	if len(first) != len(second):
		return False
	for a, b in izip(first, second):
		if selector(a) != selector(b):
			return False
	return True


# action
#--------------------------------------------------------------------------------
@linqmethod
def foreach(iterable, action):
	action = Function(action)
	for item in iterable:
		action(item)

@linqmethod
@lazymethod(Enumerable)
def do(iterable, action):
	action = Function(action)
	for item in iterable:
		action(item)
		yield item


