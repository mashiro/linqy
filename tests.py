#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import linqy
from array import array

class FunctionTests(unittest.TestCase): # {{{1
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

    def test_not(self):
        f = linqy.Not(linqy.Function(lambda x, i: x == 1))
        self.assertEqual(f.arity, 2)
        self.assertEqual(f.index, 0)
        self.assertTrue(f(2))
        self.assertFalse(f(1))


class GenerateTests(unittest.TestCase): # {{{1
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

class ProjectionTests(unittest.TestCase): # {{{1
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

class FilteringTests(unittest.TestCase): # {{{1
    def test_where(self):
        e1 = linqy.range(50,100).where(lambda x: not x % 10)
        e2 = linqy.range(50,100).where(lambda x, i: i < 5)
        e3 = linqy.make([-1,0,1])
        self.assertEqual(list(e1), [50,60,70,80,90])
        self.assertEqual(list(e2), [50,51,52,53,54])
        self.assertEqual(e3.where().tolist(), [-1,1])

    def test_oftype(self):
        e = linqy.make([1,'2',3,'4',5]).oftype(int)
        self.assertEqual(list(e), [1,3,5])

class PartitioningTests(unittest.TestCase): # {{{1
    def test_skip(self):
        e = linqy.make([1,2,3,4,5]).skip(3)
        self.assertEqual(list(e), [4,5])

    def test_skipwhile(self):
        e1 = linqy.make([1,2,3,4,5]).skipwhile(lambda x: x < 3)
        e2 = linqy.make([1,2,3,4,5]).skipwhile(lambda x, i: i < 3)
        e3 = linqy.make([1,1,0,0,1]).skipwhile()
        self.assertEqual(list(e1), [3,4,5])
        self.assertEqual(list(e2), [4,5])
        self.assertEqual(list(e3), [0,0,1])

    def test_take(self):
        e = linqy.make([1,2,3,4,5]).take(3)
        self.assertEqual(list(e), [1,2,3])

    def test_takewhile(self):
        e1 = linqy.make([1,2,3,4,5]).takewhile(lambda x: x < 3)
        e2 = linqy.make([1,2,3,4,5]).takewhile(lambda x, i: i < 3)
        e3 = linqy.make([1,1,0,0,1]).takewhile()
        self.assertEqual(list(e1), [1,2])
        self.assertEqual(list(e2), [1,2,3])
        self.assertEqual(list(e3), [1,1])

class OrderingTests(unittest.TestCase): # {{{1
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

    def make_random_range(self, min=0, max=10, col=3, row=100):
        from random import randint
        return [tuple(map(lambda x: randint(min, max), range(col))) for i in range(row)]

    def test_orderby_random1(self):
        for i in range(10):
            r = self.make_random_range()
            r1 = sorted(r, key=lambda x: x[0])
            r2 = (linqy.make(r)
                    .orderby(lambda x: x[0])
                    .tolist())
            self.assertEqual(r1, r2)

    def test_orderby_random2(self):
        for i in range(10):
            r = self.make_random_range()
            r1 = sorted(r, key=lambda x: (x[0], -x[2], x[1]))
            r2 = (linqy.make(r)
                    .orderby(lambda x: x[0])
                    .thenby_descending(lambda x: x[2])
                    .thenby(lambda x: x[1])
                    .tolist())
            self.assertEqual(r1, r2)

    def test_reverse_random(self):
        for i in range(10):
            r = self.make_random_range()
            r1 = list(reversed(r))
            r2 = linqy.make(r).reverse().tolist()
            self.assertEqual(r1, r2)


class ConcatenationTests(unittest.TestCase): # {{{1
    def test_concat(self):
        cats = [{'name': 'Barley', 'age': 8}, {'name': 'Boots', 'age': 4}, {'name': 'Whiskers', 'age': 1}]
        dogs = [{'name': 'Bounder', 'age': 3}, {'name': 'Snoopy', 'age': 14}, {'name': 'Fido', 'age': 9}]
        query = linqy.make(cats).select(lambda cat: cat['name']).concat(linqy.make(dogs).select(lambda dog: dog['name']))
        self.assertEqual(query.tolist(), ['Barley', 'Boots', 'Whiskers', 'Bounder', 'Snoopy', 'Fido'])


class EqualityTests(unittest.TestCase): # {{{1
    def test_sequenceequal(self):
        self.assertTrue(linqy.make([1,2,3]).sequenceequal(linqy.make([1,2,3])))
        self.assertFalse(linqy.make([1,2,3]).sequenceequal(linqy.make([1,2,4])))
        self.assertFalse(linqy.make([1,2,3]).sequenceequal(linqy.make([1,2])))


class QuantifierTests(unittest.TestCase): # {{{1
    def test_all(self):
        self.assertTrue(linqy.make([1,2,3,4,5]).all(lambda x: x > 0))
        self.assertTrue(linqy.make([1,2,3,4,5]).all())
        self.assertFalse(linqy.make([1,2,3,4,5]).all(lambda x: x > 3))
        self.assertTrue(linqy.empty().all(lambda x: x > 0))
        self.assertTrue(linqy.empty().all())
    
    def test_any(self):
        self.assertTrue(linqy.make([1,2,3,4,5]).any(lambda x: x > 3))
        self.assertTrue(linqy.make([1,2,3,4,5]).any())
        self.assertFalse(linqy.make([1,2,3,4,5]).any(lambda x: x > 10))
        self.assertFalse(linqy.empty().any(lambda x: x > 3))
        self.assertFalse(linqy.empty().any())

    def test_contain(self):
        self.assertTrue(linqy.make([1,2,3]).contain(1))
        self.assertTrue(linqy.make([1,2,3]).contain(2))
        self.assertTrue(linqy.make([1,2,3]).contain(3))
        self.assertFalse(linqy.make([1,2,3]).contain(4))


class ElementTests(unittest.TestCase): # {{{1
    def test_elementat(self):
        e = linqy.make([1,2,3])
        self.assertEqual(e.elementat(0), 1)
        self.assertEqual(e.elementat(1), 2)
        self.assertEqual(e.elementat(2), 3)
        self.assertRaises(IndexError, lambda: e.elementat(3))

    def test_elementat_default(self):
        e = linqy.make([1,2,3])
        self.assertEqual(e.elementat(2, 100), 3)
        self.assertEqual(e.elementat(3, 100), 100)

    def test_first(self):
        e = linqy.make([1,2,3,4,5])
        self.assertEqual(e.first(), 1)

    def test_first_pred(self):
        e = linqy.make([1,2,3,4,5])
        self.assertEqual(e.first(pred=lambda x: x > 3), 4)

    def test_first_default(self):
        e = linqy.empty()
        self.assertRaises(IndexError, lambda: e.first())
        self.assertEqual(e.first(default=100), 100)

    def test_first_pred_default(self):
        e = linqy.make([1,2,3,4,5])
        self.assertRaises(IndexError, lambda: e.first(pred=lambda x: x > 5))
        self.assertEqual(e.first(lambda x: x > 5, 100), 100)

    def test_last(self):
        e = linqy.make([1,2,3,4,5])
        self.assertEqual(e.last(), 5)

    def test_last_pred(self):
        e = linqy.make([1,2,3,4,5])
        self.assertEqual(e.last(pred=lambda x: x < 3), 2)

    def test_last_default(self):
        e = linqy.empty()
        self.assertRaises(IndexError, lambda: e.last())
        self.assertEqual(e.last(default=100), 100)

    def test_last_pred_default(self):
        e = linqy.make([1,2,3,4,5])
        self.assertRaises(IndexError, lambda: e.last(pred=lambda x: x < 0))
        self.assertEqual(e.last(lambda x: x < 0, 100), 100)

    def test_single(self):
        self.assertEqual(linqy.make([1]).single(), 1)
        self.assertRaises(ValueError, lambda: linqy.empty().single())
        self.assertRaises(ValueError, lambda: linqy.make([1,2]).single())

    def test_single_pred(self):
        self.assertEqual(linqy.range(10).single(lambda x: x == 5), 5)
        self.assertRaises(ValueError, lambda: linqy.range(10).single(lambda x: x > 5))
        self.assertRaises(ValueError, lambda: linqy.range(10).single(lambda x: x > 100))

    def test_single_default(self):
        self.assertEqual(linqy.make([1]).single(), 1)
        self.assertEqual(linqy.empty().single(default=100), 100)
        self.assertRaises(ValueError, lambda: linqy.make([1,2]).single(default=100))

    def test_single_pred_default(self):
        self.assertEqual(linqy.range(10).single(lambda x: x == 5, default=100), 5)
        self.assertRaises(ValueError, lambda: linqy.range(10).single(lambda x: x > 5, default=100))
        self.assertEqual(linqy.range(10).single(lambda x: x > 100, default=100), 100)

class ConvertionTests(unittest.TestCase): # {{{1
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

class ActionTests(unittest.TestCase): # {{{1
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


def suite(): # {{{1
    module = __import__(__name__)
    return unittest.findTestCases(module)

if __name__ == '__main__': # {{{1
    unittest.main()

