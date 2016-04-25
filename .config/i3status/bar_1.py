#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz

from pystatus import status

from pystatus import status_test

from pystatus import status_battery
from pystatus import status_brightness
from pystatus import status_cpu
from pystatus import status_datetime
from pystatus import status_disk
from pystatus import status_gpmdp
from pystatus import status_ip
from pystatus import status_netspeed
from pystatus import status_temp
from pystatus import status_volume
from pystatus import status_wifi

if __name__ == '__main__':
	bar = status.Status()

	#TODO: do I need to store all of these ids...?

	#test 			= add_to_blocks(status_test.init())

	gpmdp			= bar.add_to_blocks(status_gpmdp.init())
	wifi 			= bar.add_to_blocks(status_wifi.init(adapter_name='wlp3s0', separator=False))
	ip_wifi 		= bar.add_to_blocks(status_ip.init(adapter_name='wlp3s0'))
	#lan
	disk_tmp 		= bar.add_to_blocks(status_disk.init(path='/tmp'))
	battery 		= bar.add_to_blocks(status_battery.init(notify=False))
	brightness 		= bar.add_to_blocks(status_brightness.init())
	volume 			= bar.add_to_blocks(status_volume.init())
	temp 			= bar.add_to_blocks(status_temp.init())
	cpu 			= bar.add_to_blocks(status_cpu.init())
	datetime_local 	= bar.add_to_blocks(status_datetime.init(t_format=status_datetime.f_LONG))
	datetime_utc	= bar.add_to_blocks(status_datetime.init(timezone=pytz.utc))

	bar.run()
