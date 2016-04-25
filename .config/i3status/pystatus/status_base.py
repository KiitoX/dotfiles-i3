#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import pyautogui #pip install pyautogui

class color_class(object):
	none 		= "#FFFFFF" # White
	good 		= "#009688" # Teal
	degraded 	= "#AB47BC" # Purple 400
	bad 		= "#E91E63" # Pink

class Status(object):
	"""Status is the base class for all status modules"""
	def __init__(self, output_format, name, instance, color=color_class.none, separator=True):
		super(Status, self).__init__()
		self.fd 			= self.initFormatDict()
		self.output_format 	= self.fd.simplify(output_format)
		self.name 			= name
		self.instance 		= instance
		self.color 			= color
		self.separator 		= separator
		if self.separator:
			self.separator_block_width 	= 9 #default
		else:
			self.separator_block_width 	= 3 # ~ one space

	def initFormatDict(self):
		raise NotImplementedError('Please override the \'initFormatDict(self)\' function.')
		#return format_dict.FormatDict()

	def getOutputFormatDict(self):
		raise NotImplementedError('Please override the \'getOutputFormatDict(self)\' function.')
		#return text content

	def get(self):
		output_format_dict =  self.getOutputFormatDict()
		if output_format_dict is not None:
			return { 'name': 		self.name,
					 'instance': 	self.instance,
					 'full_text': 	self.output_format % output_format_dict,
					 'color': 		self.color,
					 'separator': 	self.separator,
					 'separator_block_width': 	self.separator_block_width}
		else:
			return None

	def onClick(self, mouse_button):
		if mouse_button == 4: #scroll up
			prev = pyautogui.position()
			pyautogui.moveTo(0, pyautogui.size()[1], pause=False)
			pyautogui.scroll(1)
			pyautogui.moveTo(*prev, pause=False)
		elif mouse_button == 5: #scroll dn
			prev = pyautogui.position()
			pyautogui.moveTo(0, pyautogui.size()[1], pause=False)
			pyautogui.scroll(-1)
			pyautogui.moveTo(*prev, pause=False)
		else: #do nothing
			pass

#simpler name for outside access
color = color_class
