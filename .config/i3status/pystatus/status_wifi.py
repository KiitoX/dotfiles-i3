#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %03.0Q%% %N', adapter_name=u'NONE',
					color_signal=False, signal_lower_threshold=-70.0, signal_upper_threshold=-67.0,
					color_quality=True, quality_lower_threshold=30.0, quality_upper_threshold=50.0, **passthrough):
		super(init, self).__init__(output_format, 'wifi', 'adapter_%s' % adapter_name, **passthrough)
		self.adapter_name 				= adapter_name
		self.color_signal 				= color_signal
		self.signal_lower_threshold 	= signal_lower_threshold
		self.signal_upper_threshold 	= signal_upper_threshold
		self.color_quality 				= color_quality
		self.quality_lower_threshold 	= quality_lower_threshold
		self.quality_upper_threshold 	= quality_upper_threshold

	quality_max = 70.0

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('N', 'ssid', 's')
		fd.add('q', 'quality_pure', 'f')
		fd.add('Q', 'quality_percent', 'f')
		fd.add('S', 'signal', 'f')
		fd.add('a', 'adapter_name', 's')
		return fd

	def getOutputFormatDict(self):
		(ssid, err) = subprocess.Popen('iwgetid %s -r' % self.adapter_name, stdout=subprocess.PIPE, shell=True).communicate()
		if len(ssid) is 0:
			#no connection / wrong adapter_name
			ssid = '-'
			self.color = color.bad
		else:
			with open('/proc/net/wireless') as file_wireless:
				for line in file_wireless:
					if line.strip().startswith(self.adapter_name):
						wifi_info = line.split()
						break
			quality = float(wifi_info[2]) # 0-70
			quality_percent = quality / self.quality_max * 100
			signal = float(wifi_info[3]) # dBm
			# not quite sure about proper coloring...
			if self.color_signal:
				if signal < self.signal_lower_threshold:
					self.color = color.bad
				elif quality < self.signal_upper_threshold:
					self.color = color.degraded
				else:
					self.color = color.good
			if self.color_quality:
				if quality_percent < self.quality_lower_threshold:
					self.color = color.bad
				elif quality_percent < self.quality_upper_threshold:
					self.color = color.degraded
				else:
					self.color = color.good
		return {'emoji': 			u'📶',
				'ssid': 			ssid.strip(),
				'quality_pure': 	quality,
				'quality_percent': 	quality_percent,
				'signal': 			signal,
				'adapter_name': 	self.adapter_name}
