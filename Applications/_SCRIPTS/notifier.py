#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import signal
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

Notify.init('notifier')

class Notification(object):
	"""docstring for Notification"""
	def __init__(self,
			name			= '-none-',
			details			= '',
			date			= datetime.datetime.now() + datetime.timedelta(minutes=5),
			repeat			= False,
			repeat_offset	= datetime.timedelta(),
			repeat_count	= 0, ### --- DON'T SET --- ###
			repeat_max		= 0, #0 == don't repeat
			local			= True,
			urgency			= Notify.Urgency.NORMAL):
		super(Notification, self).__init__()
		self.name			= name
		self.details		= details
		self.date			= date
		self.repeat			= repeat
		self.repeat_offset	= repeat_offset
		self.repeat_count	= repeat_count
		self.repeat_max		= repeat_max
		self.local			= local
		self.urgency		= urgency

	def str(self): #TODO:fix !!! FOR CHRISTS' SAKE(ricewine) !!! (never)
		return '%s %s %s %s' % (self.name, str(self.date), self.repeat, self.local)

	def in_the_past(self):
		return self.date < datetime.datetime.now()

	def time_until(self):
		return self.date - datetime.datetime.now()

	def time_remaining(self):
		return self.time_until() > datetime.timedelta()

	""" returns sleep time in seconds if notify date not reached
		returns True if it should notify now """
	def try_notify(self):
		if not self.time_remaining():
			return self.notify()
		else:
			return self.time_until().seconds

	""" returns repeat
		if repeat: changes date properly """
	def notify(self):
		if self.repeat:
			if self.repeat_max:
				if self.repeat_count < self.repeat_max:
					self.repeat_count += 1
					self._notify()
				if self.repeat_count >= self.repeat_max:
					return 'PLEASE REMOVE'
			else:
				self.repeat_count += 1
				self._notify()
			self.date += self.repeat_offset
			return 'DO NOTHING'
		else:
			self._notify()
			return 'PLEASE REMOVE'

	def _notify(self):
		n = Notify.Notification.new("%s (%s/%s)" % (self.name, self.date.time().replace(microsecond=0), datetime.datetime.now().time().replace(microsecond=0)), self.details, '') # summary, message, icon
		n.set_urgency(self.urgency)
		n.show()

def write_full_line(message):
	sys.stdout.write('% -30s\r' % message)
	sys.stdout.flush()

n_array = []

n_array.append(Notification(name			= 'Eating',
							date			= datetime.datetime.combine(datetime.date.today(), datetime.time(9, 40)),
							repeat			= True,
							repeat_offset	= datetime.timedelta(days=1)))

def init():
	pass
	#read notifications from file

def start():
	write_full_line('-> starting...')
	while True:
		sys.stdout.write('\033[5m.\033[0m')
		t_sleep = 0.1 # in seconds
		for n in n_array:
			ret = n.try_notify()
			if ret == 'PLEASE REMOVE':
				n_array.remove(n)
			if isinstance(ret, basestring):
				pass#print(ret)
			else:
				t_sleep = ret if ret < t_sleep or t_sleep == 0.1 else t_sleep
		sys.stdout.write('Sleeping for ' + str(t_sleep) + ' seconds\r')
		sys.stdout.flush()
		time.sleep(t_sleep)

def interrupted(_signo, _stack_frame):
	sys.stdout.write('\b\b\b\b')
	write_full_line('\r-> paused')
	sys.stdout.write('\ninput: ')
	_in = sys.stdin.readline().strip()
	if _in == 'exit':
		sys.exit(0)
	else:
		print("unknown input '%s'" % _in)
	signal.signal(signal.SIGINT, interrupted)
	start()
signal.signal(signal.SIGINT, interrupted)

init()
print('Ctrl+C to interrupt and input commands')
start()
