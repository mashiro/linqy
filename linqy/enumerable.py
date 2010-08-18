#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import itertools
from linqy.evaluator import Evaluator

def linqmethod(func):
	def outer(*args):
		def inner(enumerable):
			return getattr(enumerable, func.__name__)(*args)
		return inner
	globals().__setitem__(func.__name__, outer)
	return func

def lazymethod(func):
	def inner(self, *args):
		return Enumerable(lambda: func(self, *args))
	return inner

class Enumerable(object):
	def __init__(self, func):
		self._func = func
	
	def __iter__(self):
		return self._func()

	def tolist(self):
		return [item for item in self]

	@linqmethod
	def chain(self, *methods):
		return reduce(lambda e, m: m(e), [self] + list(methods))

	@lazymethod
	@linqmethod
	def select(self, selector):
		return itertools.imap(Evaluator(selector), self)

	@lazymethod
	@linqmethod
	def where(self, predicate=bool):
		return itertools.ifilter(Evaluator(predicate), self)

	@lazymethod
	@linqmethod
	def take(self, count):
		return itertools.islice(self, count)

	@lazymethod
	@linqmethod
	def takewhile(self, predicate=bool):
		return itertools.takewhile(Evaluator(predicate), self)
	
	@lazymethod
	@linqmethod
	def skip(self, count):
		return itertools.islice(self, count, None)

	@lazymethod
	@linqmethod
	def skipwhile(self, predicate=bool):
		return itertools.dropwhile(Evaluator(predicate), self)
	
	@lazymethod
	@linqmethod
	def zip(self, second):
		return itertools.izip(self, second)

	@linqmethod
	def all(self, predicate=bool):
		for item in itertools.ifilterfalse(Evaluator(predicate), self):
			return False
		return True

	@linqmethod
	def any(self, predicate=bool):
		for item in itertools.ifilter(Evaluator(predicate), self):
			return True
		return False


def make(iterable, *methods):
	''' make enumerable object from iterable object '''
	def inner():
		for item in iterable:
			yield item
	return Enumerable(lambda: inner()).chain(*methods)

@lazymethod
def range(*args):
	# xrange have'nt next() method
	return iter(xrange(*args))

@lazymethod
def repeat(item, count=None):
	if count is None:
		return itertools.repeat(item)
	else:
		return itertools.repeat(item, count)

@lazymethod
def cycle(iterable):
	return itertools.cycle(iterable)

