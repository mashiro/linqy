#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class AttributeNotFoundError(Exception): pass

def findattr(*candidates):
	for module, name in candidates:
		if isinstance(module, dict):
			if name in module:
				return module[name]
		else:
			if hasattr(module, name):
				return getattr(module, name)
	raise AttributeNotFoundError

