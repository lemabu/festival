#!/usr/bin/python
from gi.repository import GObject, Gdk

from zdf import zdf

class Network(GObject.GObject):
	id = GObject.property(type=str, default='')
	name = GObject.property(type=str, default='')
	
	def __init__(self):
		GObject.GObject.__init_(self)


class Show(GObject.GObject):
	def __init__(self):
		GObject.GObject.__init_(self)
	

class Episode(GObject.GObject):
	def __init__(self):
		GObject.GObject.__init_(self)


class SourceManager:
	""" Manages any number of video sources (different sites/networks) """
	#Importing / returning stuff from __init__ might be kinda hacky, but works
	def getAllAvailableSources(self):
		return [zdf.Source()]

