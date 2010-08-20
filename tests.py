#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest
import linqy
from linqy import Enumerable
from linqy.evaluator import Evaluator

class LinqyTests(unittest.TestCase):
	def test_eval(self):
		e1 = Evaluator(lambda n: n * 2)
		e2 = Evaluator('item * 2')
		e3 = Evaluator(lambda a ,b: a * b)
		e4 = Evaluator('first * second')
		self.assertEqual(e1(3), 6)
		self.assertEqual(e2(3), 6)
		self.assertEqual(e3(3,4), 12)
		self.assertEqual(e4(3,4), 12)

	def test_to_list(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq)
		self.assertEqual(e.to_list(), seq)

	def test_make(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq)
		self.assertTrue(isinstance(e, Enumerable))
		self.assertEqual(list(e), seq)
	
	def test_range(self):
		e1 = linqy.irange(5)
		e2 = linqy.irange(5,10)
		e3 = linqy.irange(0,10,2)
		e4 = linqy.irange(0,-5,-1)
		self.assertTrue(isinstance(e1, Enumerable))
		self.assertTrue(isinstance(e2, Enumerable))
		self.assertTrue(isinstance(e3, Enumerable))
		self.assertEqual(list(e1), [0,1,2,3,4])
		self.assertEqual(list(e2), [5,6,7,8,9])
		self.assertEqual(list(e3), [0,2,4,6,8])
		self.assertEqual(list(e4), [0,-1,-2,-3,-4])
	
	def test_count(self):
		e1 = linqy.icount().take(5)
		e2 = linqy.icount(1).take(5)
		e3 = linqy.icount(2,2).take(5)
		self.assertTrue(isinstance(e1, Enumerable))
		self.assertTrue(isinstance(e2, Enumerable))
		self.assertTrue(isinstance(e3, Enumerable))
		self.assertEqual(list(e1), [0,1,2,3,4])
		self.assertEqual(list(e2), [1,2,3,4,5])
		self.assertEqual(list(e3), [2,4,6,8,10])

	def test_repeat(self):
		e1 = linqy.irepeat(1, 5)
		e2 = linqy.irepeat(1).take(5)
		self.assertTrue(isinstance(e1, Enumerable))
		self.assertEqual(list(e1), [1,1,1,1,1])
		self.assertTrue(isinstance(e2, Enumerable))
		self.assertEqual(list(e2), [1,1,1,1,1])

	def test_cycle(self):
		e = linqy.icycle([1,2,3]).take(10)
		self.assertTrue(isinstance(e, Enumerable))
		self.assertEqual(list(e), [1,2,3,1,2,3,1,2,3,1])

	def test_select(self):
		seq = [1,2,3,4,5]
		e1 = linqy.make(seq).select(lambda n: n * 2)
		e2 = linqy.make(seq).select()
		self.assertEqual(list(e1), [2,4,6,8,10])
		self.assertEqual(list(e2), [1,2,3,4,5])
	
	def test_select_many(self):
		seq = [[1,2],[3,4],[5,6]]
		e1 = linqy.make(seq).select_many(lambda n: n)
		e2 = linqy.make(seq).select_many()
		self.assertEqual(list(e1), [1,2,3,4,5,6])
		self.assertEqual(list(e2), [1,2,3,4,5,6])

	def test_where(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).where(lambda n: n > 3)
		self.assertEqual(list(e), [4,5])
	
	def test_take(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).take(3)
		self.assertEqual(list(e), [1,2,3])

	def test_take_while(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).take_while(lambda n: n < 3)
		self.assertEqual(list(e), [1,2])

	def test_skip(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).skip(3)
		self.assertEqual(list(e), [4,5])
	
	def test_skip_while(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq).skip_while(lambda n: n < 3)
		self.assertEqual(list(e), [3,4,5])
	
	def test_zip(self):
		seq1 = [1,2,3]
		seq2 = [4,5]
		e = linqy.make(seq1).zip(seq2)
		self.assertEqual(list(e), [(1,4),(2,5)])
	
	def test_concat(self):
		seq1 = [1,2,3]
		seq2 = [4,5,6]
		e = linqy.make(seq1).concat(seq2)
		self.assertEqual(list(e), [1,2,3,4,5,6])

	def test_all(self):
		seq = [1,2,3,4,5]
		self.assertTrue(linqy.make(seq).all())
		self.assertTrue(linqy.make([]).all())
		self.assertTrue(linqy.make(seq).all(lambda n: n > 0))
		self.assertFalse(linqy.make(seq).all(lambda n: n < 3))
	
	def test_any(self):
		seq = [1,2,3,4,5]
		self.assertTrue(linqy.make(seq).any())
		self.assertFalse(linqy.make([]).any())
		self.assertTrue(linqy.make(seq).any(lambda n: n > 3))
		self.assertFalse(linqy.make(seq).any(lambda n: n < 0))
	

if __name__ == '__main__':
	unittest.main()

