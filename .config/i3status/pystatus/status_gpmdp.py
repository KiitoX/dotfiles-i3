#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socket
import websocket
from datetime import timedelta

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %a - %t [%c / %T]', **passthrough):
		super(init, self).__init__(output_format, 'music_gpmdp', 'gpmdp', **passthrough)
		self.ws = websocket.WebSocket()
		self.ws.settimeout(1)

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('a', 'artist', 's')
		fd.add('t', 'title', 's')
		fd.add('c', 'current_time', 's')
		fd.add('T', 'total_time', 's')
		return fd

	def getOutputFormatDict(self):
		#custom code
		name = 'music_gpmdp'
		playing = self.getWebSocketChannel('playState')
		if playing is not None:
			if playing:
				song = self.getWebSocketChannel('song')
				time = self.getWebSocketChannel('time')
				artist 			= song['artist']
				title 			= song['title']
				current_time 	= str(timedelta(seconds=time['current'] / 1000))
				total_time 		= str(timedelta(seconds=time['total'] / 1000))
			else: # minimal websocket channels
				# with open('/home/manuel/.config/Google Play Music Desktop Player/json_store/playback.json') as file_playback:
				# 	info = json.loads(file_playback.read())
				artist 			= u'x' # info['song']['artist']
				title 			= u'x' # info['song']['title']
				current_time 	= u'0' # str(timedelta(seconds=info['time']['current'] / 1000))
				total_time 		= u'0' # str(timedelta(seconds=info['time']['total'] / 1000))
			return {'emoji': 		u'▸' if playing else u'▪', # ⏹⏸⏯ 🎶
					'artist': 		artist,
					'title': 		title,
					'current_time': current_time,
					'total_time': 	total_time}
		else:
			return None

	# ['playState', 'shuffle', 'repeat', 'song', 'time']
	def getWebSocketChannel(self, channel):
		try:
			self.ws.connect('ws://localhost:5672')
			j = json.loads(self.ws.recv())
			while (j['channel'] != channel):
				j = json.loads(self.ws.recv())
			return j['payload']
		except websocket._exceptions.WebSocketTimeoutException:
			return None # no more content to be received
		except websocket._exceptions.WebSocketException:
			return None # other websocket exception
		except socket.error:
			return None # socket not open / invalid url
		except ValueError:
			return None # received payload not json
