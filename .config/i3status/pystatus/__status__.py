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

	#OPTIONAL
	def onClick(self, mouse_button): #remove unused button blocks to pass down to super
		if mouse_button == 1: #left click
			pass
		elif mouse_button == 2: #right click
			pass
		elif mouse_button == 3: #middle click
			pass
		elif mouse_button == 4: #scroll up
			pass
		elif mouse_button == 5: #scroll dn
			pass
		else:
			super(init, self).onClick(mouse_button)
