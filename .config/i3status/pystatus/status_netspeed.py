#!/usr/bin/env python
# -*- coding: utf-8 -*-

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e [%r | %t]', adapter_name=u'NONE', **passthrough):
		super(init, self).__init__(output_format, 'netspeed', 'adapter_%s' % adapter_name, **passthrough)
		self.adapter_name 				= adapter_name
		self.prev_receive_bytes 		= 0
		self.prev_receive_packets 		= 0
		self.prev_transmit_bytes 		= 0
		self.prev_transmit_packets 		= 0

	decimal		= 1000.0
	binary		= 1024.0
	ending		= {decimal: ['B/s', 'kB/s', 'MB/s', 'GB/s'], binary: ['B/s', 'KiB/s', 'MiB/s', 'GiB/s']}

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji_down_up', 's')
		fd.add('E', 'emoji_up_down', 's')
		fd.add('r', 'receive_bytes', 's')
		fd.add('R', 'receive_packets', 's')
		fd.add('t', 'transmit_bytes', 's')
		fd.add('T', 'transmit_packets', 's')
		fd.add('a', 'adapter_name', 's')
		return fd

	def getOutputFormatDict(self):
		net_info = None
		with open('/proc/net/dev') as file_dev:
			for line in file_dev:
				if line.strip().startswith(self.adapter_name):
					net_info = line.split()
					break
		if net_info is not None:
			receive_bytes 		= float(net_info[1])
			receive_packets 	= float(net_info[2])
			transmit_bytes 		= float(net_info[9])
			transmit_packets 	= float(net_info[10])
			diff_receive_bytes 		= receive_bytes 	- self.prev_receive_bytes
			diff_receive_packets 	= receive_packets 	- self.prev_receive_packets
			diff_transmit_bytes 	= transmit_bytes 	- self.prev_transmit_bytes
			diff_transmit_packets 	= transmit_packets 	- self.prev_transmit_packets
			self.prev_receive_bytes 	= receive_bytes
			self.prev_receive_packets 	= receive_packets
			self.prev_transmit_bytes 	= transmit_bytes
			self.prev_transmit_packets 	= transmit_packets
			return {'emoji_down_up': 	u'⇵',
					'emoji_up_down': 	u'⇅',
					'receive_bytes': 	self.getReadable(diff_receive_bytes, self.binary),
					'receive_packets': 	self.getReadable(diff_receive_packets, self.binary),
					'transmit_bytes': 	self.getReadable(diff_transmit_bytes, self.binary),
					'transmit_packets': self.getReadable(diff_transmit_packets, self.binary),
					'adapter_name': 	self.adapter_name}
		else:
			return None

	def getReadable(self, byte, space_format):
		i = 0
		while byte > space_format:
			if i+1 < len(self.ending):
				byte = byte / space_format
				i += 1
			else:
				break
		return (u'%.0f%s' if i < 1 else u'%.1f%s') % (byte, self.ending[space_format][i])
