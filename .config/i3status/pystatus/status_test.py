#!/usr/bin/env python
# -*- coding: utf-8 -*-

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e default', **passthrough):
		super(init, self).__init__(output_format, 'module_name', 'module_instance(details)', **passthrough)

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		return fd

	def getOutputFormatDict(self):
		#custom code
		return {'emoji': u'emoji'}
