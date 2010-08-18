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
		return list(self)

	@linqmethod
	def combine(self, *methods):
		return reduce(lambda e, m: m(e), [self] + list(methods))

	@linqmethod
	def select(self, selector):
		return iselect(self, selector)

	@linqmethod
	def where(self, predicate=bool):
		return iwhere(self, predicate)

	@linqmethod
	def take(self, count):
		return itake(self, count)

	@linqmethod
	def takewhile(self, predicate=bool):
		return itakewhile(self, predicate)
	
	@linqmethod
	def skip(self, count):
		return iskip(self, count)

	@linqmethod
	def skipwhile(self, predicate=bool):
		return iskipwhile(self, predicate)
	
	@linqmethod
	def zip(self, *iterables):
		return izip(self, *iterables)

	@linqmethod
	def all(self, predicate=bool):
		return iall(self, predicate)

	@linqmethod
	def any(self, predicate=bool):
		return iany(self, predicate)


def make(iterable, *methods):
	''' make enumerable object from iterable object '''
	def inner():
		for item in iterable:
			yield item
	return Enumerable(lambda: inner()).combine(*methods)

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



@lazymethod
def iselect(iterable, selector):
	return itertools.imap(Evaluator(selector), iterable)

@lazymethod
def iwhere(iterable, predicate):
	return itertools.ifilter(Evaluator(predicate), iterable)

@lazymethod
def itake(iterable, count):
	return itertools.islice(iterable, count)

@lazymethod
def itakewhile(iterable, predicate):
	return itertools.takewhile(Evaluator(predicate), iterable)

@lazymethod
def iskip(iterable, count):
	return itertools.islice(iterable, count, None)

@lazymethod
def iskipwhile(iterable, predicate):
	return itertools.dropwhile(Evaluator(predicate), iterable)

def iall(iterable, predicate=bool):
	for item in itertools.ifilterfalse(Evaluator(predicate), iterable):
		return False
	return True

def iany(iterable, predicate=bool):
	for item in itertools.ifilter(Evaluator(predicate), iterable):
		return True
	return False

@lazymethod
def izip(*iterables):
	return itertools.izip(*iterables)

