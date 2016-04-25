#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import fcntl
import struct

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%i', adapter_name=u'NONE', **passthrough):
		super(init, self).__init__(output_format, 'ip', 'adapter_%s' % adapter_name, **passthrough)
		self.adapter_name = adapter_name

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('i', 'ip_local', 's')
		return fd

	def getOutputFormatDict(self):
		socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ip_local = socket.inet_ntoa(fcntl.ioctl(socket_.fileno(),
					0x8915, struct.pack('256s', bytes(self.adapter_name[:15])))[20:24])
		return {'emoji': 		u'none', #TODO: maybe find a fitting ip emoji
				'ip_local': 	ip_local}
