#!/usr/bin/env python
# -*- coding: utf-8 -*-

import format_dict
from status_base import Status
from status_base import color

cpu_cores = 4

class init(Status):
	def __init__(self, output_format=u'%e %.1c%%', threshold=90, cpu_line=0, **passthrough):
		super(init, self).__init__(output_format, 'cpu_usage', 'cpu_%d' % cpu_line, **passthrough)
		self.threshold 	= threshold
		self.cpu_line 	= cpu_line % cpu_cores
		self.prev_total = 0
		self.prev_idle 	= 0

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('c', 'cpu', 'f')
		return fd

	def getOutputFormatDict(self):
		try:
			with open('/proc/stat') as file_stat:
				cpu_info = file_stat.readlines()[self.cpu_line].strip().split()
			# user   (1) | nice   (2) | system (3) | idle   (4)
			curr_idle 		= float(cpu_info[4])
			curr_total 		= float(cpu_info[1]) + float(cpu_info[2]) + float(cpu_info[3]) + curr_idle
			diff_idle 		= curr_idle - self.prev_idle
			diff_total 		= curr_total - self.prev_total
			diff_usage 		= (1000 * (diff_total - diff_idle) / diff_total + 5) / 10 if diff_total else 0
			self.prev_total = curr_total
			self.prev_idle 	= curr_idle
			cpu = diff_usage
		except IOError as e: #should never ever fire, kept just cause
			cpu = -1.0
		if cpu >= float(self.threshold):
			self.color = color.bad
		else:
			self.color = color.none
		return {'emoji': 	u'📊',
				'cpu': 		cpu}
