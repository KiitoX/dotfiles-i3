#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal
import sys
import json
import select
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

class Status(object):
	"""docstring for Status"""
	def __init__(self):
		super(Status, self).__init__()
		self.blocks = {}
		self.header = {
			'version': 1,
			'stop_signal': signal.SIGTSTP,
			'cont_signal': signal.SIGCONT,
			'click_events': True
		}
		self.running = True
		self.interrupted = False
		self.updates = 1 			# updates per second
		Notify.init('status_bar')
		self.n = Notify.Notification.new('Status Bar', 'First click, this can\'t be processed properly, click again', 'dialog-information')

	def add_to_blocks(self, status):
		identifier = '%s_%s' % (status.name, status.instance)
		self.blocks.update({identifier: {'status': status, 'pos': len(self.blocks)}})
		return identifier

	def create_info_array(self): #TODO: implement some caching, to allow for differing update timeouts
		array = [0]*len(self.blocks)
		for block_id in self.blocks:
			array[self.blocks[block_id]['pos']] = self.blocks[block_id]['status'].get()
		return filter(None, array)

	def print_line(self, message):
		""" Non-buffered printing to stdout. """
		sys.stdout.write(message + '\n')
		sys.stdout.flush()

	def read_messages(self):
		ready = select.select([sys.stdin], [], [], 0)[0]
		if ready:
			for raw_line in ready:
				line = raw_line.readline().strip()
				if line:
					if line.startswith('['):# init line
						self.n.show()
						pass # do nothing
					elif line.startswith('{'):# first line
						pass # THIS ONE DOESN'T SEND PROPERLY... NO FIX AVAILABLE CURRENTLY
						#self.handle_message(json.loads(line))
					elif line.startswith(','):# rest lines
						self.handle_message(json.loads(line[1:]))
				else: # an empty line means stdin has been closed
					sys.exit(3)

	def handle_message(self, message):
		#TODO: some default actions maybe, possibly do them in the status_base class but that'd propably be confusing
		self.blocks['%s_%s' % (message['name'], message['instance'])]['status'].onClick(message['button'])
		#message['x'] & message['y'] if I want to do popup stuff...

	def run(self):
		signal.signal(signal.SIGTERM, self.sigterm_handler)
		signal.signal(signal.SIGQUIT, self.sigquit_handler)
		signal.signal(signal.SIGINT,  self.sigint_handler)
		signal.signal(signal.SIGTSTP, self.sigtstp_handler)
		signal.signal(signal.SIGCONT, self.sigcont_handler)
		signal.signal(signal.SIGUSR1, self.sigusr1_handler)

		self.print_line(json.dumps(self.header)) 							# version header
		self.print_line('[') 											# start of infinite array
		self.print_line(json.dumps(self.create_info_array()))				# starting line

		while self.running:
			while self.interrupted:
				self.wait(self.updates*10)#long wait
			self.print_line(',' + json.dumps(self.create_info_array()))
			for i in range(0, 10):#TODO: temporary solution to better react to click_events, remove after caching is solved
				self.read_messages()
				self.wait(self.updates/10.0)

		self.print_line('] ')

	def cleanup(self, _signo, _stack_frame):
		self.running, self.interrupted = False, False

	def pause(self, _signo, _stack_frame, pause_state):
		self.interrupted = pause_state

	def sigterm_handler(self, _signo, _stack_frame):
		self.cleanup(_signo, _stack_frame)

	def sigquit_handler(self, _signo, _stack_frame):
		self.cleanup(_signo, _stack_frame)

	def sigint_handler(self, _signo, _stack_frame):
		self.cleanup(_signo, _stack_frame)

	def sigtstp_handler(self, _signo, _stack_frame):
		self.pause(_signo, _stack_frame, True)

	def sigcont_handler(self, _signo, _stack_frame):
		self.pause(_signo, _stack_frame, False)

	def sigusr1_handler(self, _signo, _stack_frame):
		self.print_line(',' + json.dumps(self.create_info_array()))

	def wait(self, s):
		'''Wait until the next increment of n seconds'''
		x = time.time()
		time.sleep(s-(x%s))
