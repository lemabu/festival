from gi.repository import Gtk, GObject

class MainWindow(Gtk.Window):
	def __init__(self, callback):
		Gtk.Window.__init__(self, title="Hello World")

		self.button = Gtk.Button(label="Click Here")
		self.button.connect("clicked", self.on_button_clicked)
		self.add(self.button)

		self.cb=callback

	def on_button_clicked(self, widget):
		self.cb(self, widget)

