#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

import sys
import select

import re

import time

var = 'NO'

print('{"stop_signal": 20, "cont_signal": 18, "click_events": true, "version": 1}')
print('[')
print('[{"name": "debug", "full_text": "DEBUG; CLICK ME! (%s)"}]' % var)

while True:
	with open('/home/manuel/.config/i3status/logp', 'a') as log:
		# in_, out_, error_ = select.select( [sys.stdin], [], [], 0 )
		# if sys.stdin in in_:
		# 	sys.stdout.flush()
		# 	line_in = raw_input()
		# 	# = sys.stdin.readline()
		# 	if line_in:
		# 		if line_in.startswith('['): #start
		# 			var = '%s | %s' % (time.time(), line_in.strip())
		# 			sys.stdout.flush()
		# 			in_, out_, error_ = select.select( [sys.stdin], [], [], 0 )
		# 			testp = 'NO'
		# 			if sys.stdin in in_:
		# 				sys.stdout.flush()
		# 				line_in = raw_input()
		# 				if line_in:
		# 					testp = line_in
		# 				else:
		# 					testp = 'empty line'
		# 			else:
		# 				testp = 'not found'
		# 			log.write('***%s***%s***\n' % (time.time(), testp))
		# 		else:
		# 			var = '%s | %s' % (time.time(), line_in.strip())
		# 		log.write('***%s***%s***\n' % (time.time(), line_in))
		sys.stdin.open()
		read = subprocess.Popen('read -t 0 varname; echo $varname', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		(line_in, err) = subprocess.Popen(['read', '-t', '0'], stdout=subprocess.PIPE, stdin=subprocess.PIPE).communicate()

		if line_in:
			log.write('***%s***%s***\n' % (time.time(), line_in))
			var = '%s | %s' % (time.time(), line_in.strip())
		else:
			var = '%s | ' % (time.time())

		print(',[{"name": "debug", "full_text": "DEBUG; CLICK ME! (%s)"}]' % (re.sub('"', '\'', var)))
