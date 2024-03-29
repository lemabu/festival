#!/usr/bin/python
from gi.repository import Gtk, GObject, Gdk, Gio

from ui.mainwindow import MainWindow

import media.source.zdf.zdf as ZDF

import threading

class FestivalApp(Gtk.Application):
	__builder = ""
	__source_ZDF = ""
	
	__playButtonConnection = None
	
	__lastShowPath = ""
	__lastEpisodePath = ""
	
	#UI signal handlers implementation	
	def handleShowSelectionChange(self, showList):
		path, col = showList.get_cursor()
		if path is not None:
			if path.to_string() != self.__lastShowPath:
				self.__lastShowPath = path.to_string()
			else:
				return
			self.__source_ZDF.setSelectedShow(path, self.__builder.get_object("teaserimageview"))
			self.__builder.get_object("episodelistview").set_visible(True)
			self.__builder.get_object("teaserimageview").set_visible(True)
		else:
			self.__builder.get_object("teaserimageview").set_visible(False)
			
	def handlePlayButtonPress(self, playButton, episode):
		#print(episode.mediaUrl)
		Gio.AppInfo.get_default_for_type("video/mp4", True).launch_uris((episode.mediaUrl,),None)

	def handleEpisodeSelectionChange(self, episodeList):
		print "handleEpisodeSelectionChange running in "+threading.current_thread().name
		path, col = episodeList.get_cursor()
		if path is not None:
			if self.__playButtonConnection is not None:
				self.__builder.get_object("episodeplaybutton").disconnect(self.__playButtonConnection)
			episode = self.__source_ZDF.getEpisode(path)
			self.__builder.get_object("episodedatelabel").set_text(episode.pubDate)
			self.__builder.get_object("episodetitlelabel").set_text(episode.title)
			self.__builder.get_object("episodedetailslabel").set_text(episode.description)
			self.__playButtonConnection = self.__builder.get_object("episodeplaybutton").connect("clicked",self.handlePlayButtonPress,episode)
			self.__builder.get_object("episodedetailbox").set_visible(True)
			self.__builder.get_object("hbuttonbox1").set_visible(True)
			self.__builder.get_object("episodetitlelabel").set_visible(True)
			self.__builder.get_object("episodedatelabel").set_visible(True)
			self.__builder.get_object("episodedetailslabel").set_visible(True)
		else:
			self.__builder.get_object("episodetitlelabel").set_text("")
			self.__builder.get_object("episodedatelabel").set_text("")
			self.__builder.get_object("episodedetailslabel").set_text("")
			self.__builder.get_object("hbuttonbox1").set_visible(False)

	#UI signal handlers declaration
	__handlers = {
		"onDeleteWindow": Gtk.main_quit
	}
	
	def __init__(self):
		Gtk.Application.__init__(self, application_id="apps.cau.festival", flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.connect("activate", self.on_activate)
	def on_activate(self, data=None):
		Gdk.threads_enter()
		#Load UI definition from XML
		self.__builder = Gtk.Builder()
		self.__builder.add_from_file("ui/xml/mainwindow.xml")
		#Connect signals
		self.__builder.connect_signals(self.__handlers)
		#Get all Sources / set store
		self.__source_ZDF = ZDF.Source()
		showStore = self.__source_ZDF.getShows()
		episodeStore = self.__source_ZDF.getEpisodes()

		showList = self.__builder.get_object("showlistview")
		showList.set_model(showStore)
		#showList.set_model(self.__showsStore)
		titleRenderer = Gtk.CellRendererText()
		detailsRenderer = Gtk.CellRendererText()
		titleColumn = Gtk.TreeViewColumn("Sendung", titleRenderer, text=1)
		datailsColumn = Gtk.TreeViewColumn("Details", detailsRenderer, text=2)
		showList.append_column(titleColumn)
		showList.append_column(datailsColumn)
		showList.connect("cursor-changed",self.handleShowSelectionChange)
		
		episodeList = self.__builder.get_object("episodelistview")
		episodeList.set_model(episodeStore)
		episodeTitleRenderer = Gtk.CellRendererText()
		episodeTitleColumn = Gtk.TreeViewColumn("Folgen", episodeTitleRenderer, text=2)
		episodeList.append_column(episodeTitleColumn)
		episodeList.connect("cursor-changed",self.handleEpisodeSelectionChange)


		window = self.__builder.get_object("MainWindow")
		window.show()
		self.add_window(window)
		Gdk.threads_leave()
		


if __name__ == '__main__':
	GObject.threads_init()
	Gdk.threads_init()
	festival = FestivalApp()
	festival.run(None)

