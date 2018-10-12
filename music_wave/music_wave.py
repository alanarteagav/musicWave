import main_window_controller

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

if __name__=='__main__':
    main_controller = main_window_controller.MainWindowController()
    main_controller.start()
    Gtk.main()
