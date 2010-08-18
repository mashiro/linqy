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

	@linqmethod
	def chain(self, *methods):
		return reduce(lambda e, m: m(e), [self] + list(methods))

	@lazymethod
	@linqmethod
	def select(self, selector):
		evaluator = Evaluator(selector)
		return itertools.imap(evaluator, self)

	@lazymethod
	@linqmethod
	def where(self, predicate=bool):
		evaluator = Evaluator(predicate)
		return itertools.ifilter(evaluator, self)

	@lazymethod
	@linqmethod
	def take(self, count):
		return itertools.islice(self, count)

	@lazymethod
	@linqmethod
	def takewhile(self, predicate=bool):
		evaluator = Evaluator(predicate)
		return itertools.takewhile(evaluator, self)
	
	@lazymethod
	@linqmethod
	def skip(self, count):
		return itertools.islice(self, count, None)

	@lazymethod
	@linqmethod
	def skipwhile(self, predicate=bool):
		evaluator = Evaluator(predicate)
		return itertools.dropwhile(evaluator, self)
	
	@lazymethod
	@linqmethod
	def zip(self, second):
		return itertools.izip(self, second)

	@linqmethod
	def all(self, predicate=bool):
		evaluator = Evaluator(predicate)
		for item in itertools.ifilterfalse(evaluator, self):
			return False
		return True

	@linqmethod
	def any(self, predicate=bool):
		evaluator = Evaluator(predicate)
		for item in itertools.ifilter(evaluator, self):
			return True
		return False

def make(iterable, *methods):
	def inner():
		for item in iterable:
			yield item
	return Enumerable(lambda: inner()).chain(*methods)

@lazymethod
def repeat(item, count):
	return itertools.repeat(item, count)

@lazymethod
def cycle(iterable):
	return itertools.cycle(iterable)

