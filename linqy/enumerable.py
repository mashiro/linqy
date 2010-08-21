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
next = findattr((__builtins__, 'next'), lambda x: x.next())
xrange = findattr((__builtins__, 'xrange'), range)


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
	return iter(xrange(s.start or 0, s.stop or sys.maxsize, s.step or 1))

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
def iselect(iterable, selector=None):
	evaluator = Evaluator(selector)
	for item in iterable:
		yield evaluator(item)

@lazymethod
def iselect_many(iterable, selector=None):
	for it in iselect(iterable, selector):
		for item in it:
			yield item

@lazymethod
def iwhere(iterable, pred=bool):
	return itertools.ifilter(Evaluator(pred), iterable)

@lazymethod
def itake(iterable, count):
	return itertools.islice(iterable, count)

@lazymethod
def itake_while(iterable, pred=bool):
	return itertools.takewhile(Evaluator(pred), iterable)

@lazymethod
def iskip(iterable, count):
	return itertools.islice(iterable, count, None)

@lazymethod
def iskip_while(iterable, pred=bool):
	return itertools.dropwhile(Evaluator(pred), iterable)

@lazymethod
def izip(*iterables):
	return itertools.izip(*iterables)

@lazymethod
def iconcat(*iterables):
	return itertools.chain(*iterables)

@lazymethod
def iorder_by(iterable, key=None):
	if key is None:
		return iter(sorted(iterable, key=None))
	else:
		return iter(sorted(iterable, key=Evaluator(key)))

@lazymethod
def ireverse(iterable):
	return reversed(list(iterable))

def iall(iterable, pred=bool):
	for item in itertools.ifilterfalse(Evaluator(pred), iterable):
		return False
	return True

def iany(iterable, pred=bool):
	for item in itertools.ifilter(Evaluator(pred), iterable):
		return True
	return False

def ifirst(iterable, pred=None):
	evaluator = Evaluator(pred)
	it = iter(iterable)
	try:
		while True:
			item = next(it)
			if pred is None or evaluator(item):
				return item
	except StopIteration:
		raise IndexError

def ilast(iterable, pred=None):
	return ifirst(ireverse(iterable), pred)


class Enumerable(object): # {{{1
	def __init__(self, func):
		self._func = func
	
	def __iter__(self):
		return self._func()

	def to_list(self):
		return list(self)

	@linqmethod
	def combine(self, *methods):
		return functools.reduce(lambda e, m: m(e), [self] + list(methods))

	@linqmethod
	def select(self, selector=None):
		return iselect(self, selector)

	@linqmethod
	def select_many(self, selector=None):
		return iselect_many(self, selector)

	@linqmethod
	def where(self, pred=bool):
		return iwhere(self, pred)

	@linqmethod
	def take(self, count):
		return itake(self, count)

	@linqmethod
	def take_while(self, pred=bool):
		return itake_while(self, pred)
	
	@linqmethod
	def skip(self, count):
		return iskip(self, count)

	@linqmethod
	def skip_while(self, pred=bool):
		return iskip_while(self, pred)

	@linqmethod
	def zip(self, *iterables):
		return izip(self, *iterables)

	@linqmethod
	def concat(self, *iterables):
		return iconcat(self, *iterables)

	@linqmethod
	def reverse(self):
		return ireverse(self)

	@linqmethod
	def order_by(self, key=None):
		return iorder_by(self, key=key)

	@linqmethod
	def all(self, pred=bool):
		return iall(self, pred)

	@linqmethod
	def any(self, pred=bool):
		return iany(self, pred)

	@linqmethod
	def first(self, pred=None):
		return ifirst(self, pred)

	@linqmethod
	def last(self, pred=None):
		return ilast(self, pred)
	
