#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest
import linqy
from array import array

class FunctionTests(unittest.TestCase):
	def test_identity(self):
		f = linqy.Function(None)
		self.assertFalse(f)
		self.assertEqual(f.arity, 1)
		self.assertEqual(f.index, 0)
		self.assertEqual(f(2), 2)
		self.assertEqual(f.index, 1)

	def test_lambda(self):
		f = linqy.Function(lambda x, y: x * y)
		self.assertTrue(f)
		self.assertEqual(f.arity, 2)
		self.assertEqual(f.index, 0)
		self.assertEqual(f(2,3), 6)
		self.assertEqual(f.index, 1)

	def test_method(self):
		class inner(object):
			def f(self, x, y):
				return x * y
		f = linqy.Function(inner().f)
		self.assertTrue(f)
		self.assertEqual(f.arity, 2)
		self.assertEqual(f.index, 0)
		self.assertEqual(f(2,3), 6)
		self.assertEqual(f.index, 1)

class ConvertionTests(unittest.TestCase):
	def test_asenumerable(self):
		self.assertTrue(isinstance(linqy.asenumerable([1,2,3]), linqy.SequenceEnumerable))
		self.assertTrue(isinstance(linqy.asenumerable(linqy.make([1,2,3])), linqy.Enumerable))
		self.assertFalse(isinstance(linqy.asenumerable(linqy.range(5)), linqy.SequenceEnumerable))

	def test_toarray(self):
		e = linqy.make([1,2,3,4,5])
		self.assertEqual(e.toarray('i'), array('i', [1,2,3,4,5]))

	def test_tolist(self):
		e = linqy.make([1,2,3,4,5])
		self.assertEqual(e.tolist(), [1,2,3,4,5])
	
class EqualityTests(unittest.TestCase):
	def test_sequenceequal(self):
		self.assertTrue(linqy.make([1,2,3]).sequenceequal(linqy.make([1,2,3])))
		self.assertFalse(linqy.make([1,2,3]).sequenceequal(linqy.make([1,2,4])))
		self.assertFalse(linqy.make([1,2,3]).sequenceequal(linqy.make([1,2])))

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
		e1 = linqy.make([1,2,3]).select(lambda x: x * 2)
		e2 = linqy.make([1,2,3]).select(lambda x, i: (i, i * x))
		self.assertEqual(list(e1), [2,4,6])
		self.assertEqual(list(e2), [(0,0),(1,2),(2,6)])
	
	def test_selectmany(self):
		e1 = linqy.make([1,2,3]).selectmany(lambda x: [x, x * 2])
		e2 = linqy.make([1,2,3]).selectmany(lambda x, i: [(i, x), i * x])
		e3 = linqy.make([1,2,3]).selectmany(lambda x: range(x), result=lambda x, y: y)
		self.assertEqual(list(e1), [1,2,2,4,3,6])
		self.assertEqual(list(e2), [(0,1),0,(1,2),2,(2,3),6])
		self.assertEqual(list(e3), [0,0,1,0,1,2])
	
	def test_zip(self):
		e = linqy.make([1,2,3]).zip([4,5,6])
		self.assertEqual(list(e), [(1,4),(2,5),(3,6)])
	
	def test_enumerate(self):
		e = linqy.make([1,2,3]).enumerate()
		self.assertEqual(list(e), [(0,1),(1,2),(2,3)])

class FilteringTests(unittest.TestCase):
	def test_where(self):
		e1 = linqy.range(50,100).where(lambda x: not x % 10)
		e2 = linqy.range(50,100).where(lambda x, i: i < 5)
		self.assertEqual(list(e1), [50,60,70,80,90])
		self.assertEqual(list(e2), [50,51,52,53,54])
	
	def test_oftype(self):
		e = linqy.make([1,'2',3,'4',5]).oftype(int)
		self.assertEqual(list(e), [1,3,5])
	
class OrderingTests(unittest.TestCase):
	@classmethod
	def makeseq(cls):
		return [{'id': 1, 'name':  'apple', 'price': 100, 'num':  8},
				{'id': 2, 'name': 'orange', 'price': 100, 'num': 10},
				{'id': 3, 'name':  'apple', 'price': 120, 'num':  8},
				{'id': 4, 'name': 'orange', 'price': 120, 'num':  8},
				{'id': 5, 'name': 'orange', 'price':  80, 'num': 10}]

	def test_orderby(self):
		seq = self.makeseq()
		a,b,c,d,e = seq
		enum = linqy.make(seq).orderby(lambda x: x['name'])
		self.assertEqual(list(enum), [a,c,b,d,e])

	def test_orderby_descending(self):
		seq = self.makeseq()
		a,b,c,d,e = seq
		enum = linqy.make(seq).orderby_descending(lambda x: x['name'])
		self.assertEqual(list(enum), [b,d,e,a,c])
	
	def test_thenby(self):
		seq = self.makeseq()
		a,b,c,d,e = seq
		enum = linqy.make(seq).orderby(lambda x: x['name']).thenby(lambda x: x['price'])
		self.assertEqual(list(enum), [a,c,e,b,d])
		self.assertRaises(AttributeError, lambda: linqy.range(10).thenby(lambda x: x))

	def test_thenby_descending(self):
		seq = self.makeseq()
		a,b,c,d,e = seq
		enum = linqy.make(seq).orderby(lambda x: x['name']).thenby_descending(lambda x: x['price'])
		self.assertEqual(list(enum), [c,a,d,b,e])
		self.assertRaises(AttributeError, lambda: linqy.range(10).thenby_descending(lambda x: x))
	
	def test_orderby_thenby(self):
		seq = self.makeseq()
		a,b,c,d,e = seq
		enum = (linqy.make(seq)
				.orderby(lambda x: x['num'])
				.thenby(lambda x: x['price'])
				.thenby_descending(lambda x: x['name']))
		self.assertEqual(list(enum), [a,d,c,e,b])
	
	def test_reverse(self):
		seq = linqy.make([1,2,3,4,5])
		e1 = seq.reverse()
		e2 = e1.reverse()
		e3 = e2.reverse()
		self.assertEqual(list(e1), [5,4,3,2,1])
		self.assertEqual(list(e2), [1,2,3,4,5])
		self.assertTrue(linqy.sequenceequal(e1, e3))

class PartitioningTests(unittest.TestCase):
	def test_skip(self):
		e = linqy.make([1,2,3,4,5]).skip(3)
		self.assertEqual(list(e), [4,5])
	
	def test_skipwhile(self):
		e1 = linqy.make([1,2,3,4,5]).skipwhile(lambda x: x < 3)
		e2 = linqy.make([1,2,3,4,5]).skipwhile(lambda x, i: i < 3)
		self.assertEqual(list(e1), [3,4,5])
		self.assertEqual(list(e2), [4,5])
	
	def test_take(self):
		e = linqy.make([1,2,3,4,5]).take(3)
		self.assertEqual(list(e), [1,2,3])

	def test_takewhile(self):
		e1 = linqy.make([1,2,3,4,5]).takewhile(lambda x: x < 3)
		e2 = linqy.make([1,2,3,4,5]).takewhile(lambda x, i: i < 3)
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

		e = linqy.make([1,2,3]).do(self.addi)
		self.assertEqual(self.num, 6)
		list(e)
		self.assertEqual(self.num, 12)

	def test_foreach(self):
		linqy.make([1,2,3]).foreach(self.add)
		self.assertEqual(self.num, 6)

		linqy.make([1,2,3]).foreach(self.addi)
		self.assertEqual(self.num, 12)
	
	
def suite():
	suite = unittest.TestSuite()
	for v in globals().values():
		if isinstance(v, type) and issubclass(v, unittest.TestCase):
			suite.addTests(unittest.makeSuite(v))
	return suite

if __name__ == '__main__':
	unittest.main()

