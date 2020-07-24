#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import tkinter as tk

###############################################################################
class Application(tk.Frame):
    ###########################################################################
    def __init__(self, main=None):
        tk.Frame.__init__(self, main)
        self.pack()
        self.createWidgets()
    ###########################################################################
    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")
    ###########################################################################
    def say_hi(self):
        print("hi there, everyone!")
###############################################################################

root = tk.Tk()
app = Application(main=root)
app.mainloop()