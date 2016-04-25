#!/usr/bin/env python
# -*- coding: utf-8 -*-

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %b/%m', brightness_max=255, **passthrough):
		super(init, self).__init__(output_format, 'brightness', 'max_%d' % brightness_max, **passthrough)
		self.brightness_max 	= brightness_max
		self.brightness_half 	= brightness_max / 2

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('b', 'brightness', 'd')
		fd.add('m', 'brightness_max', 'd')
		return fd

	def getOutputFormatDict(self):
		try:
			with open('/sys/class/backlight/radeon_bl0/brightness') as file_brightness:
				brightness = int(file_brightness.readlines()[0].strip())
		except IOError:
			brightness = -1
		return {'emoji': 			u'☀️ ' if brightness >= self.brightness_half else u'☼',
				'brightness': 		brightness,
				'brightness_max': 	self.brightness_max}
