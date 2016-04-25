#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %u / %t', path='/', color_percentage=True, min_threshold=5, lower_threshold=60, upper_threshold=90, **passthrough):
		super(init, self).__init__(output_format, 'disk_capacity', 'path_%s' % path, **passthrough)
		self.path 				= path
		self.color_percentage 	= color_percentage
		self.min_threshold 		= min_threshold
		self.lower_threshold 	= lower_threshold
		self.upper_threshold 	= upper_threshold

	decimal 	= 1000.0
	binary 		= 1024.0
	ending 		= {decimal: ['\b', 'kB', 'MB', 'GB', 'TB', 'PB'], binary: ['\b', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']}

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('p', 'path', 's')
		fd.add('P', 'percentage', 'f')
		fd.add('u', 'used_binary', 's')
		fd.add('U', 'used_decimal', 's')
		fd.add('t', 'total_binary', 's')
		fd.add('T', 'total_decimal', 's')
		fd.add('f', 'free_binary', 's')
		fd.add('F', 'free_decimal', 's')
		return fd

	def getOutputFormatDict(self):
		st 			= os.statvfs(self.path)
		free 		= st.f_bavail * st.f_frsize
		total 		= st.f_blocks * st.f_frsize
		used 		= (st.f_blocks - st.f_bfree) * st.f_frsize
		percentage 	= float(used) / float(total) * 100
		if self.color_percentage:
			if percentage >= float(self.upper_threshold):
				self.color = color.bad
			elif percentage >= float(self.lower_threshold):
				self.color = color.degraded
			elif percentage >= float(self.min_threshold):
				self.color = color.none
			else:
				self.color = color.good
		return {'emoji': 			u'💾',
				'path': 			self.path,
				'percentage': 		percentage,
				'used_binary':		self.getReadable(used, self.binary),
				'used_decimal': 	self.getReadable(used, self.decimal),
				'total_binary': 	self.getReadable(total, self.binary),
				'total_decimal': 	self.getReadable(total, self.decimal),
				'free_binary': 		self.getReadable(free, self.binary),
				'free_decimal': 	self.getReadable(free, self.decimal)}

	def getReadable(self, byte, space_format):
		i = 0
		while byte > space_format:
			if i+1 < len(self.ending):
				byte = byte / space_format
				i += 1
			else:
				break
		return u'%.1f %s' % (byte, self.ending[space_format][i])
