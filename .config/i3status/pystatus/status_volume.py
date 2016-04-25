#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import alsaaudio

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %v%%', **passthrough):
		super(init, self).__init__(output_format, 'volume', 'device_main', **passthrough)

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('v', 'volume', 'd')
		return fd

	def getOutputFormatDict(self):
		muted 	= self.equalize(alsaaudio.Mixer().getmute())
		volume 	= self.equalize(alsaaudio.Mixer().getvolume())
		if muted:
			self.color = color.degraded
		else:
			self.color = color.none
		return {'emoji': 	u'🔇' if muted or volume <= 0 else u'🔈' if volume < 50 else u'🔉',
				'volume': 	volume}

	def equalize(self, v):
		return int((v[0] + v[1]) / 2)

	def onClick(self, mouse_button):
		if mouse_button == 1: #left click
			subprocess.Popen('/home/manuel/.config/i3/do.sh vol_mt', shell=True)
		elif mouse_button == 4: #scroll up
			subprocess.Popen('/home/manuel/.config/i3/do.sh vol_up 10', shell=True)
		elif mouse_button == 5: #scroll dn
			subprocess.Popen('/home/manuel/.config/i3/do.sh vol_dn 10', shell=True)
		else:
			super(init, self).onClick(mouse_button)
