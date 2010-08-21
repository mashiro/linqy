#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class AttributeNotFoundError(Exception):
	pass

def findattr(*candidates):
	for candidate in candidates:
		if isinstance(candidate, tuple):
			module, name = candidate
			if isinstance(module, dict):
				if name in module:
					return module[name]
			else:
				if hasattr(module, name):
					return getattr(module, name)
		else:
			return candidate
	raise AttributeNotFoundError

