#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, subprocess

from gi.repository import Gtk, Gio
from gi.repository import GLib

###############################################################################
class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World")
#______________________________________________________________________________
#
def test_1():
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
###############################################################################
class Handler():
    def __init__(self, cmd):
        self.cmd = CommandTextView(cmd)

    def on_button1_clicked(self, widget):
        self.cmd.run()
        pass

    def on_button2_clicked(self, widget):
        pass

    def on_textview1_add(self, widget):
        widget.inset
        pass

    def on_window1_delete_event(self, *args):
        Gtk.main_quit(*args)
###############################################################################
class CommandTextView(Gtk.TextView):
    ''' NICE TEXTVIEW THAT READS THE OUTPUT OF A COMMAND SYNCRONOUSLY '''
    def __init__(self, command):
        '''COMMAND : THE SHELL COMMAND TO SPAWN'''
        super(CommandTextView, self).__init__()
        self.command = command
    def run(self):
        ''' RUNS THE PROCESS '''
        proc = subprocess.Popen(self.command, stdout = subprocess.PIPE) # SPAWNING
        GLib.io_add_watch(proc.stdout, # FILE DESCRIPTOR
                          GLib.IO_IN,  # CONDITION
                          self.write_to_buffer) # CALLBACK
    def write_to_buffer(self, fd, condition):
        if condition == GLib.IO_IN: #IF THERE'S SOMETHING INTERESTING TO READ
        #CZ#char = fd.read(1) # WE READ ONE BYTE PER TIME, TO AVOID BLOCKING
            char = fd.read().decode("utf-8")
            buff = self.get_buffer()
            buff.insert_at_cursor(char) # WHEN RUNNING DON'T TOUCH THE TEXTVIEW!!
            return True # FUNDAMENTAL, OTHERWISE THE CALLBACK ISN'T RECALLED
        else:
            return False # RAISED AN ERROR: EXIT AND I DON'T WANT TO SEE YOU ANYMORE
#______________________________________________________________________________
#
def test_2():
    cmd = CommandTextView("find")

    win = Gtk.Window()
    win.connect("delete-event", lambda wid, event: Gtk.main_quit()) # DEFINING CALLBACKS WITH LAMBDAS
    win.set_size_request(200,300)
    win.add(cmd)
    win.show_all()

    cmd.run()
    Gtk.main()
#______________________________________________________________________________
#
def test_3():
    cmd = CommandTextView("find")

    builder = Gtk.Builder()
    builder.add_from_file("test-gui-Gtk.glade")
    builder.connect_signals(Handler(cmd))

    window = builder.get_object("window1")
    window.show_all()

    cmd.run()
    Gtk.main()
###############################################################################
class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Stack Demo")
    #CZ#Gtk.Window.__init__(self, title="Stack Demo", type=Gtk.WINDOW_TOPLEVEL)
        self.set_border_width(10)
        self.set_default_size(400, 200)
    #CZ#self.has_toplevel_focus()

        #hb = Gtk.HeaderBar()
        #hb.props.show_close_button = True
        #hb.props.title = "HeaderBar example"
        #self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        #hb.pack_end(button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        #hb.pack_start(box)

        self.add(Gtk.TextView())
#______________________________________________________________________________
#
def test_4():
    win = HeaderBarWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
#______________________________________________________________________________
#
if __name__ == '__main__':
    test_4()