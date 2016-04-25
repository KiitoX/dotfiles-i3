#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import pytz
import tzlocal # $ pip install pytz

import format_dict
from status_base import Status
from status_base import color

LOCAL = tzlocal.get_localzone()

f_LONG  = '%F %a %T %Z'
f_SHORT = '%T %Z'

class init(Status):
	def __init__(self, output_format=u'%e %t', timezone=LOCAL, t_format=f_SHORT, **passthrough):
		super(init, self).__init__(output_format, 'datetime', 'timezone_%s' % timezone, **passthrough)
		self.timezone = timezone
		self.t_format = t_format

	def initFormatDict(self):
		fd = format_dict.FormatDict()
		fd.add('e', 'emoji', 's')
		fd.add('t', 'time', 's')
		return fd

	def getOutputFormatDict(self):
		#custom code
		time = datetime.now(self.timezone)
		return {'emoji': 	self.getEmoji(time),
				'time': 	time.strftime(self.t_format)}

	def getEmoji(self, time):
		base = 0x1F550
		base = base + time.hour % 12 - 1
		base = base + 12 if base < 0x1F550 else base
		base = base + 12 if time.minute >= 30 else base
		return unichr(base)
