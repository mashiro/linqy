#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# imports {{{1
import functools
import itertools
from linqy.evaluator import Evaluator
from linqy.utils import findattr

# hack {{{1
functools.reduce = findattr((functools, 'reduce'), (__builtins__, 'reduce'))
itertools.izip = findattr((itertools, 'izip'), (__builtins__, 'zip'))
itertools.ifilter = findattr((itertools, 'ifilter'), (__builtins__, 'filter'))
itertools.imap = findattr((itertools, 'imap'), (__builtins__, 'map'))
itertools.ifilterfalse = findattr((itertools, 'ifilterfalse'), (itertools, 'filterfalse'))


# decorators {{{1
def linqmethod(func):
	@functools.wraps(func)
	def outer(*args, **kargs):
		def inner(enumerable):
			return getattr(enumerable, func.__name__)(*args, **kargs)
		return inner
	globals().__setitem__(func.__name__, outer)
	return func

def lazymethod(func):
	@functools.wraps(func)
	def inner(*args, **kargs):
		return Enumerable(lambda: func(*args, **kargs))
	return inner


# functios {{{1
def make(iterable, *methods):
	''' make enumerable from iterable '''
	def inner():
		for item in iterable:
			yield item
	return Enumerable(lambda: inner()).combine(*methods)

@lazymethod
def irange(*args):
	''' make enumerable range '''
	s = slice(*args)
	return iter(range(s.start or 0, s.stop or sys.maxsize, s.step or 1))

@lazymethod
def icount(start=0, step=1):
	n = start
	while True:
		yield n
		n += step

@lazymethod
def irepeat(item, count=None):
	if count is None:
		return itertools.repeat(item)
	else:
		return itertools.repeat(item, count)

@lazymethod
def icycle(iterable):
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

@lazymethod
def izip(*iterables):
	return itertools.izip(*iterables)

@lazymethod
def iconcat(*iterables):
	return itertools.chain(*iterables)

def iall(iterable, predicate=bool):
	for item in itertools.ifilterfalse(Evaluator(predicate), iterable):
		return False
	return True

def iany(iterable, predicate=bool):
	for item in itertools.ifilter(Evaluator(predicate), iterable):
		return True
	return False


class Enumerable(object): # {{{1
	def __init__(self, func):
		self._func = func
	
	def __iter__(self):
		return self._func()

	def tolist(self):
		return list(self)

	@linqmethod
	def combine(self, *methods):
		return functools.reduce(lambda e, m: m(e), [self] + list(methods))

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
	def concat(self, *iterables):
		return iconcat(self, *iterables)

	@linqmethod
	def all(self, predicate=bool):
		return iall(self, predicate)

	@linqmethod
	def any(self, predicate=bool):
		return iany(self, predicate)
	
