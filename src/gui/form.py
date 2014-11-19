import sys

# try:
#     import pygtk
#     pygtk.require("2.0")
# except:
#     pass
#
# try:
#     import gtk
#     # import gtk.glade
# except:
#     sys.exit(1)


# import pgi
# pgi.install_as_gi()
# from gi.repository import Gtk, GObject

from gi.repository import Gtk

GLADE_MARKUP = 'os-simulator.glade'


class OsSimulatorWindow(object):
    def __init__(self, builder):
        super(OsSimulatorWindow, self).__init__()
        self.builder = builder
        self.builder.connect_signals(self)
        self.window = builder.get_object('os_simulator_window')

    def show(self):
        self.window.show_all()

    def on_os_simulator_window_destroy(*args):
        Gtk.main_quit(*args)


if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file(GLADE_MARKUP)
    window = OsSimulatorWindow(builder)
    window.show()
    Gtk.main()
