#!/usr/bin/env python
# -*- coding: utf-8 -*-

# additional i3status wrapper

import sys
import json
import datetime
import pytz
import websocket
import socket
import alsaaudio
import string

# emoji markers:
#   battery:
#	 <⚡ - charging>
#   volume:
#	 <🔊 - high>
#   cpu:
#	 <📈 - up>
#	 <📉 - down>
#	  📊 - all
#	 <🎚 - all>

reload(sys)
sys.setdefaultencoding('utf8')

def getMusic():
	return u'🎶'

ws = websocket.WebSocket()

def get_gpmdp_channel(channel):
	try:
		ws.connect('ws://localhost:5672')
		j = json.loads(ws.recv())
		while (j['channel'] != channel):
			j = json.loads(ws.recv())
		return j['payload']
	except socket.error, ValueError:
		return False

def get_music():
	try:
		s = get_gpmdp_channel('song')
		t = get_gpmdp_channel('time')
		info = json.loads(open('/home/manuel/.config/Google Play Music Desktop Player/json_store/playback.json').read())
		return u'%s - %s [%s]' % (s['artist'], s['title'], get_remaining_readable(t))
	except ValueError:
		return u''

def get_remaining_readable(time):
	return u'%s / %s' % (millis_to_minutes(time['current']), millis_to_minutes(time['total']))

def millis_to_minutes(millis):
	x = int(millis) / 1000
	seconds = (x % 60).__str__()
	x = x / 60
	val = u':' + seconds if len(seconds) == 2 else u':0' + seconds
	minutes = (x % 60).__str__()
	x = x / 60
	val = minutes + val if len(minutes) == 2 else u'0' + minutes + val
	hours = x % 24
	val = u'%s:' % (hours) + val if hours > 0 else val
	return val

def getWifi():
	return u'📶'

def getEthernet():
	return u'🔌'

def getDiskTemp():
	return u'💾'

def getBattery():
	return u'🔌 ' if int(get_charging()) else u'🔋'

def get_charging():
	with open('/sys/class/power_supply/ACAD/online') as fp:
		return fp.readlines()[0].strip()

# hh:mm:ss
def get_remaining(time):
	return '~' if int(string.split(time, ':')[0]) > 8 else time[0:-2]+'00'

def get_battery():
	with open('/sys/class/power_supply/BAT1/capacity') as fp:
		return fp.readlines()[0].strip()
	return 'N/A'

def getBrightness():
	return u'☀️ ' if int(get_brightness()) >= 128 else u'☼'

def get_brightness():
	with open('/sys/class/backlight/radeon_bl0/brightness') as fp:
		return fp.readlines()[0].strip()

def getVolume():
	return u'🔇' if int(get_volume()) <= 0 else u'🔉' if int(get_volume()) >= 50 else u'🔈'

def get_volume():
	v = alsaaudio.Mixer().getvolume()[0]
	m = alsaaudio.Mixer().getmute()[0]
	return -1 if m == 1L else v

def getTemp():
	return u'🌡'

def get_temp():
	#/sys/devices/virtual/thermal/thermal_zone0/temp	#VirtualDevice
	#/sys/class/hwmon/hwmon3/temp1_input				#PCI Adapter
	with open('/sys/class/hwmon/hwmon3/temp1_input') as fp:
		c = float(fp.readlines()[0].strip())
		c = c / 1000
		return "%.1f°C" % c
	return 'N/A'

def getCpu():
	return u'📊'

def getTime():
	base = 0x1F550
	base = base + get_hour() -1
	base = base + 12 if base < 0x1F550 else base
	base = base + 12 if get_minute() >= 30 else base
	return unichr(base)

def get_hour():
	return datetime.datetime.now().hour % 12

def get_minute():
	return datetime.datetime.now().minute

def getTimeUTC():
	base = 0x1F550
	base = base + get_hour_utc() -1
	base = base + 12 if base < 0x1F550 else base
	base = base + 12 if get_minute_utc() >= 30 else base
	return unichr(base)

def get_hour_utc():
	return datetime.datetime.now(pytz.utc).hour % 12

def get_minute_utc():
	return datetime.datetime.now(pytz.utc).minute

def print_line(message):
	""" Non-buffered printing to stdout. """
	sys.stdout.write(message + '\n')
	sys.stdout.flush()

def read_line():
	""" Interrupted respecting reader for stdin. """
	# try reading a line, removing any extra whitespace
	try:
		line = sys.stdin.readline().strip()
		# i3status sends EOF, or an empty line
		if not line:
			sys.exit(3)
		return line
	# exit on ctrl-c
	except KeyboardInterrupt:
		sys.exit()

if __name__ == '__main__':
	# Skip the first line which contains the version header.
	print_line(read_line())

	# The second line contains the start of the infinite array.
	print_line(read_line())

	while True:
		line, prefix = read_line(), ''
		# ignore comma at start of lines
		if line.startswith(','):
			line, prefix = line[1:], ','

		j = json.loads(line)
		# insert information into the start of the json, but could be anywhere

		#type().__name__
		i = 0

		if get_gpmdp_channel('playState'):
			#music
			j.insert(i, {'full_text' : '%s %s' % (getMusic(), get_music()), 'name' : 'music'})
			i += 1
		#wifi
		j[i].update({'full_text' : '%s %s' % (getWifi(), j[i].get('full_text'))})
		i += 1
		#ethernet
		j[i].update({'full_text' : '%s %s' % (getEthernet(), j[i].get('full_text'))})
		i += 1
		#disk /tmp/
		j[i].update({'full_text' : '%s %s' % (getDiskTemp(), j[i].get('full_text'))})
		i += 1
		#battery
		j[i].update({'full_text' : '%s %s%% %s' % (getBattery(), get_battery(), get_remaining(j[i].get('full_text')))})
		i += 1
		#brightness
		j.insert(i, {'full_text' : '%s %s/255' % (getBrightness(), get_brightness()), 'name' : 'brightness'})
		i += 1
		#volume
		j[i].update({'full_text' : '%s %s' % (getVolume(), j[i].get('full_text'))})
		i += 1
		#temp
		j.insert(i, {'full_text' : '%s %s' % (getTemp(), get_temp()), 'name' : 'temp'})
		i += 1
		#cpu
		j[i].update({'full_text' : '%s %s.0' % (getCpu(), j[i].get('full_text'))})
		i += 1
		#time local
		j[i].update({'full_text' : '%s %s' % (getTime(), j[i].get('full_text'))})
		i += 1
		#time utc
		j[i].update({'full_text' : '%s %s' % (getTimeUTC(), j[i].get('full_text'))})
		i += 1

		# and echo back new encoded json
		print_line(prefix+json.dumps(j))
