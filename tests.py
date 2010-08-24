#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest
import linqy

class EvaluatorTests(unittest.TestCase):
	def test_bool(self):
		e1 = linqy.Evaluator(lambda n: n * 2)
		e2 = linqy.Evaluator(None)
		self.assertTrue(e1)
		self.assertFalse(e2)
		self.assertTrue(bool(e1))
		self.assertFalse(bool(e2))

	def test_eval(self):
		e1 = linqy.Evaluator(lambda n: n * 2)
		e2 = linqy.Evaluator('_ * 2')
		e3 = linqy.Evaluator(lambda x, y: x * y)
		e4 = linqy.Evaluator('_1 * _2')
		self.assertEqual(e1(2), 4)
		self.assertEqual(e2(2), 4)
		self.assertEqual(e3(2,3), 6)
		self.assertEqual(e4(2,3), 6)

class EqualityTests(unittest.TestCase):
	def test_sequence_equal(self):
		self.assertTrue(linqy.make([1,2,3]).sequence_equal(linqy.make([1,2,3])))
		self.assertFalse(linqy.make([1,2,3]).sequence_equal(linqy.make([1,2,4])))
		self.assertFalse(linqy.make([1,2,3]).sequence_equal(linqy.make([1,2])))

class GenerateTests(unittest.TestCase):
	def test_make(self):
		e = linqy.make([1,2,3])
		self.assertTrue(isinstance(e, linqy.Enumerable))
		self.assertEqual(list(e), [1,2,3])
	
	def test_empty(self):
		e = linqy.empty()
		self.assertTrue(isinstance(e, linqy.Enumerable))
		self.assertEqual(list(e), [])
	
	def test_range(self):
		e1 = linqy.range(3)
		e2 = linqy.range(3, 6)
		e3 = linqy.range(1, 6, 2)
		self.assertTrue(isinstance(e1, linqy.Enumerable))
		self.assertTrue(isinstance(e2, linqy.Enumerable))
		self.assertTrue(isinstance(e3, linqy.Enumerable))
		self.assertEqual(list(e1), [0,1,2])
		self.assertEqual(list(e2), [3,4,5])
		self.assertEqual(list(e3), [1,3,5])
	
	def test_repeat(self):
		e1 = linqy.repeat(1, 3)
		e2 = linqy.repeat(1).take(3)
		self.assertTrue(isinstance(e1, linqy.Enumerable))
		self.assertTrue(isinstance(e2, linqy.Enumerable))
		self.assertEqual(list(e1), [1,1,1])
		self.assertEqual(list(e2), [1,1,1])

	def test_cycle(self):
		e = linqy.cycle([1,2,3]).take(10)
		self.assertTrue(isinstance(e, linqy.Enumerable))
		self.assertEqual(list(e), [1,2,3,1,2,3,1,2,3,1])
	
	def test_countup(self):
		e1 = linqy.countup().take(3)
		e2 = linqy.countup(3).take(3)
		e3 = linqy.countup(3,3).take(3)
		e4 = linqy.countup(3,-3).take(3)
		self.assertTrue(isinstance(e1, linqy.Enumerable))
		self.assertTrue(isinstance(e2, linqy.Enumerable))
		self.assertTrue(isinstance(e3, linqy.Enumerable))
		self.assertTrue(isinstance(e4, linqy.Enumerable))
		self.assertEqual(list(e1), [0,1,2])
		self.assertEqual(list(e2), [3,4,5])
		self.assertEqual(list(e3), [3,6,9])
		self.assertEqual(list(e4), [3,0,-3])

class ProjectionTests(unittest.TestCase):
	def test_select(self):
		e1 = linqy.make([1,2,3]).select('_ * 2')
		e2 = linqy.make([1,2,3]).select('(_2, _2 * _1)', enum=True)
		e3 = linqy.make([1,2,3]).select(lambda x, i: (i, i * x), enum=True)
		self.assertEqual(list(e1), [2,4,6])
		self.assertEqual(list(e2), [(0,0),(1,2),(2,6)])
		self.assertEqual(list(e3), [(0,0),(1,2),(2,6)])
	
	def test_selectmany(self):
		e1 = linqy.make([1,2,3]).selectmany('[_, _ * 2]')
		e2 = linqy.make([1,2,3]).selectmany('[(_2, _1), _2 * _1]', enum=True)
		e3 = linqy.make([1,2,3]).selectmany(lambda x, i: [(i, x), i * x], enum=True)
		e4 = linqy.make([1,2,3]).selectmany(lambda x: range(x), result=lambda x, y: y)
		self.assertEqual(list(e1), [1,2,2,4,3,6])
		self.assertEqual(list(e2), [(0,1),0,(1,2),2,(2,3),6])
		self.assertEqual(list(e3), [(0,1),0,(1,2),2,(2,3),6])
		self.assertEqual(list(e4), [0,0,1,0,1,2])
	
	def test_zip(self):
		e = linqy.make([1,2,3]).zip([4,5,6])
		self.assertEqual(list(e), [(1,4),(2,5),(3,6)])
	
	def test_enumerate(self):
		e = linqy.make([1,2,3]).enumerate()
		self.assertEqual(list(e), [(0,1),(1,2),(2,3)])

class FilteringTests(unittest.TestCase):
	def test_where(self):
		e1 = linqy.range(50,100).where('not _ % 10')
		e2 = linqy.range(50,100).where('_2 < 5', enum=True)
		self.assertEqual(list(e1), [50,60,70,80,90])
		self.assertEqual(list(e2), [50,51,52,53,54])
	
	def test_oftype(self):
		e = linqy.make([1,'2',3,'4',5]).oftype(int)
		self.assertEqual(list(e), [1,3,5])
	
class PartitioningTests(unittest.TestCase):
	def test_skip(self):
		e = linqy.make([1,2,3,4,5]).skip(3)
		self.assertEqual(list(e), [4,5])
	
	def test_skipwhile(self):
		e1 = linqy.make([1,2,3,4,5]).skipwhile('_ < 3')
		e2 = linqy.make([1,2,3,4,5]).skipwhile('_2 < 3', enum=True)
		self.assertEqual(list(e1), [3,4,5])
		self.assertEqual(list(e2), [4,5])
	
	def test_take(self):
		e = linqy.make([1,2,3,4,5]).take(3)
		self.assertEqual(list(e), [1,2,3])

	def test_takewhile(self):
		e1 = linqy.make([1,2,3,4,5]).takewhile('_ < 3')
		e2 = linqy.make([1,2,3,4,5]).takewhile('_2 < 3', enum=True)
		self.assertEqual(list(e1), [1,2])
		self.assertEqual(list(e2), [1,2,3])

class ActionTests(unittest.TestCase):
	def setUp(self):
		self.num = 0

	def add(self, x):
		self.num += x

	def addi(self, x, i):
		self.num += x

	def test_do(self):
		e = linqy.make([1,2,3]).do(self.add)
		self.assertEqual(self.num, 0)
		list(e)
		self.assertEqual(self.num, 6)

		e = linqy.make([1,2,3]).do(self.addi, enum=True)
		self.assertEqual(self.num, 6)
		list(e)
		self.assertEqual(self.num, 12)

	def test_foreach(self):
		linqy.make([1,2,3]).foreach(self.add)
		self.assertEqual(self.num, 6)

		linqy.make([1,2,3]).foreach(self.addi, enum=True)
		self.assertEqual(self.num, 12)
	
class FunctorTests(unittest.TestCase):
	def test_make(self):
		from linqy.functors import select, where
		e = linqy.make([1,2,3,4,5],
			where(lambda x: x > 3),
			select(lambda x: x * 2))
		self.assertEqual(list(e), [8,10])

	def test_combine(self):
		from linqy.functors import select, where
		e = linqy.make([1,2,3,4,5]).combine(
			where(lambda x: x > 3),
			select(lambda x: x * 2))
		self.assertEqual(list(e), [8,10])

	
def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.makeSuite(EvaluatorTests))
	suite.addTests(unittest.makeSuite(EqualityTests))
	suite.addTests(unittest.makeSuite(GenerateTests))
	suite.addTests(unittest.makeSuite(ProjectionTests))
	suite.addTests(unittest.makeSuite(FilteringTests))
	suite.addTests(unittest.makeSuite(PartitioningTests))
	suite.addTests(unittest.makeSuite(ActionTests))
	suite.addTests(unittest.makeSuite(FunctorTests))
	return suite

if __name__ == '__main__':
	unittest.main()

