#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest
import linqy
from linqy import Enumerable
from linqy.evaluator import Evaluator

class LinqyTests(unittest.TestCase):
	def test_eval(self):
		e1 = Evaluator('item * 2')
		e2 = Evaluator(lambda n: n * 2)
		self.assertEqual(e1(2), 4)
		self.assertEqual(e2(2), 4)

	def test_tolist(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq)
		self.assertEqual(e.tolist(), seq)

	def test_make(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq)
		self.assertTrue(isinstance(e, Enumerable))
		self.assertEqual(list(e), seq)
	
	def test_range(self):
		e1 = linqy.range(5)
		e2 = linqy.range(5,10)
		e3 = linqy.range(0,10,2)
		self.assertTrue(isinstance(e1, Enumerable))
		self.assertTrue(isinstance(e2, Enumerable))
		self.assertTrue(isinstance(e3, Enumerable))
		self.assertEqual(list(e1), [0,1,2,3,4])
		self.assertEqual(list(e2), [5,6,7,8,9])
		self.assertEqual(list(e3), [0,2,4,6,8])

	def test_repeat(self):
		e1 = linqy.repeat(1, 5)
		e2 = linqy.repeat(1).take(5)
		self.assertTrue(isinstance(e1, Enumerable))
		self.assertEqual(list(e1), [1,1,1,1,1])
		self.assertTrue(isinstance(e2, Enumerable))
		self.assertEqual(list(e2), [1,1,1,1,1])

	def test_cycle(self):
		e = linqy.cycle([1,2,3]).take(10)
		self.assertTrue(isinstance(e, Enumerable))
		self.assertEqual(list(e), [1,2,3,1,2,3,1,2,3,1])

	def test_select(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).select(lambda n: n * 2)
		self.assertEqual(list(e), [2,4,6,8,10])

	def test_where(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).where(lambda n: n > 3)
		self.assertEqual(list(e), [4,5])

if __name__ == '__main__':
	unittest.main()

