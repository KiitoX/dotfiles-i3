#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz

from pystatus import status

from pystatus import status_battery
from pystatus import status_cpu
from pystatus import status_datetime
from pystatus import status_netspeed
from pystatus import status_temp
from pystatus import status_volume

if __name__ == '__main__':
	bar = status.Status()

	netspeed_wifi 	= bar.add_to_blocks(status_netspeed.init(adapter_name='wlp3s0'))
	battery 		= bar.add_to_blocks(status_battery.init(notify=True))
	volume 			= bar.add_to_blocks(status_volume.init())
	temp 			= bar.add_to_blocks(status_temp.init())
	cpu 			= bar.add_to_blocks(status_cpu.init())
	datetime_local 	= bar.add_to_blocks(status_datetime.init())

	bar.run()
