#!/usr/bin/env python
# -*- coding: utf-8 -*-

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %.1T\u00B0C', sensor_name='hwmon3', color_percentage=True, min_threshold=60, lower_threshold=75, upper_threshold=90, **passthrough):
		super(init, self).__init__(output_format, 'temp', 'sensor_%s' % sensor_name, **passthrough)
		self.sensor_name 		= sensor_name
		self.color_percentage 	= color_percentage
		self.min_threshold 		= min_threshold
		self.lower_threshold 	= lower_threshold
		self.upper_threshold 	= upper_threshold

	UNKNOWN_TEMP = -1

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('t', 'temp', 's')
		fd.add('T', 'temp_raw', 'f')
		return fd

	def getOutputFormatDict(self):
		try:
			#/sys/devices/virtual/thermal/thermal_zone0/temp	#VirtualDevice
			#/sys/class/hwmon/hwmon3/temp1_input				#PCI Adapter
			with open('/sys/class/hwmon/%s/temp1_input' % self.sensor_name) as file_temp1_input:
				temp = float(file_temp1_input.readline().strip())
			temp = temp / 1000
		except IOError as e: #should never ever fire, kept just cause
			temp = self.UNKNOWN_TEMP
		if self.color_percentage:
			if temp >= float(self.upper_threshold):
				self.color = color.bad
			elif temp >= float(self.lower_threshold):
				self.color = color.degraded
			elif temp >= float(self.min_threshold):
				self.color = color.none
			else:
				self.color = color.good
		return {'emoji': 	u'🌡',
				'temp': 	'N/A' if temp is self.UNKNOWN_TEMP else '%.1f',
				'temp_raw': temp}
