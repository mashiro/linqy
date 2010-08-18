#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest
import linqy

class LinqyTests(unittest.TestCase):
	def test_make(self):
		seq = [1,2,3,4,5]
		e = linqy.make(seq)
		self.assertTrue(isinstance(e, linqy.Enumerable))
		self.assertEqual(list(e), seq)

if __name__ == '__main__':
	unittest.main()

