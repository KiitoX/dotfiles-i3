#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

import format_dict
from status_base import Status
from status_base import color

class init(Status):
	def __init__(self, output_format=u'%e %c%% %R', notify=False, threshold=30, time_threshold=timedelta(hours=8), **passthrough):
		super(init, self).__init__(output_format, 'battery', 'notify_%s' % notify, **passthrough)
		self.notify 		= notify
		self.threshold 		= threshold
		self.time_threshold = time_threshold
		if self.notify:
			self.battery_notification = 0
			Notify.init('status_battery')
			self.n = Notify.Notification.new('Battery', 'Battery level' 'dialog-information')
			self.n.set_urgency(Notify.Urgency.CRITICAL)

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('c', 'capacity', 's')
		fd.add('r', 'remaining', 's')
		fd.add('R', 'remaining_short', 's')
		return fd

	def getOutputFormatDict(self):
		try:
			with open('/sys/class/power_supply/ACAD/online') as file_online:
				charging = int(file_online.readline().strip())
		except IOError as e: #should never ever fire, kept just cause
			charging = 0
		try:
			with open('/sys/class/power_supply/BAT1/capacity') as file_capacity:
				capacity = int(file_capacity.readline().strip())
		except IOError as e: # no battery found
			capacity = -1
		remaining = self.calcRemaining(charging)
		remaining_short = '~' if remaining.total_seconds() > self.time_threshold.total_seconds() or remaining is timedelta.min else str(remaining)
		if self.notify:
			self.updateNotification(charging, capacity, remaining)
		if capacity <= self.threshold:
			self.color = color.bad
		else:
			self.color = color.none
		return {'emoji': 			u'🔌 ' if charging else u'🔋',
				'capacity': 		capacity if capacity >= 0 else 'N/A',
				'remaining': 		remaining,
				'remaining_short': 	remaining_short}

	def updateNotification(self, charging, capacity, remaining):
		if charging:
			self.battery_notification = 0
			self.n.close()
		elif self.battery_notification != capacity and capacity <= self.threshold:
			self.battery_notification = capacity
			self.n.update('Battery low', 'Battery is at %i%% (%s remaining)' % (capacity, remaining), 'dialog-information')
			self.n.show()

	def calcRemaining(self, charging):
		try:
			with open('/sys/class/power_supply/BAT1/charge_full') as file_charge_full:
				charge_full = float(file_charge_full.readline().strip())
			with open('/sys/class/power_supply/BAT1/charge_now') as file_charge_now:
				charge_now  = float(file_charge_now.readline().strip())
			with open('/sys/class/power_supply/BAT1/current_now') as file_current_now:
				current_now = float(file_current_now.readline().strip())
			with open('/sys/class/power_supply/BAT1/voltage_now') as file_voltage_now:
				voltage_now = float(file_voltage_now.readline().strip())
			current_now = (voltage_now / 1000.0) * (current_now / 1000.0)
			if voltage_now != -1:
				charge_now = (voltage_now / 1000.0) * (charge_now / 1000.0)
				charge_full = (voltage_now / 1000.0) * (charge_full / 1000.0)
			if current_now > 0:
				if charging:
					remaining_time = timedelta(hours=((charge_full - charge_now) / current_now), milliseconds=0)
				else:
					remaining_time = timedelta(hours=(charge_now / current_now), milliseconds=0)
				return remaining_time - timedelta(microseconds=remaining_time.microseconds)
			return timedelta.min
		except IOError as e:
			return timedelta.min
