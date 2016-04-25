#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FormatDict(object):
	"""FormatDict is a helper class to make optional formats viable"""
	def __init__(self):
		super(FormatDict, self).__init__()
		self.format_dict = {}
		self.format_dict['%'] = {'full_id': '', 'type_id': '%'}

	def add(self, simple_id, full_id, type_id):
		self.format_dict[simple_id] = {'full_id': '(%s)' % full_id, 'type_id': type_id}

	def addDefaults(self):
		self.add('')

	def simplify(self, simple_string):
		s_iter = (c for c in simple_string)
		keep = u''
		new_string = u''
		for c in s_iter:
			new_string += c
			if c == u'%':
				try:
					s_id = next(s_iter)
					while s_id not in self.format_dict:
						keep += s_id
						s_id = next(s_iter)
					new_string += u'%(full_id)s%(keep)s%(type_id)s' % dict(self.format_dict[s_id], keep=keep)
					keep = u''
				except StopIteration:
					raise SyntaxError('Failed to parse format: \'%s\'' % simple_string)
		return new_string
