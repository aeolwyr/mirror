#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, GdkPixbuf
from gi.repository.Gdk import ModifierType

import touch, screen

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Mirror')
        self.img = Gtk.Image()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.img)
        self.add(scrolled_window)

        def mouse_notify(widget, event, action):
            if action == 'm' and not event.state & ModifierType.BUTTON1_MASK:
                # movement events are only valid when the button is pressed
                return False

            pixbuf = self.img.get_pixbuf()
            # translate the coordinates
            size = self.get_size()
            x_min = (size.width - pixbuf.get_width()) / 2
            x = (event.x - x_min) / pixbuf.get_width()
            if x < 0 or x > 1: return False
            y_min = (size.height - pixbuf.get_height()) / 2
            y = (event.y - y_min) / pixbuf.get_height()
            if y < 0 or y > 1: return False
            self.touch.send(action, x, y)
            return True

        self.connect('motion-notify-event', mouse_notify, 'm')
        self.connect('button-press-event', mouse_notify, 'd')
        self.connect('button-release-event', mouse_notify, 'u')

        self.touch = touch.Client()
        screen.receive(self.load)

    def load(self, stream):
        size = self.get_size()
        GdkPixbuf.Pixbuf.new_from_stream_at_scale_async(
                stream, size.width, size.height, True, None,
                self.load_finish)

    def load_finish(self, source, result):
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream_finish(result)
        self.img.set_from_pixbuf(pixbuf)

window = MainWindow()
window.connect('delete-event', Gtk.main_quit)
window.show_all()

Gtk.main()
