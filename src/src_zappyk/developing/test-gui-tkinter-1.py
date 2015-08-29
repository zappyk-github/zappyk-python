#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

from tkinter import *

root_title    = "Hi test"
root_geometry = "200x85"
root_geometry = "200x180"

###############################################################################
class App:
    ###########################################################################
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.lbl = Label(frame, text="Hello World!\n")
        self.lbl.pack()

        self.button = Button(frame, text="Quit", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Say hi!", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        self.space = Text(frame)
        self.space.pack(side=BOTTOM)
    ###########################################################################
    def say_hi(self):
        print("Hello!")
###############################################################################
root = Tk()
root.title(root_title)
#root.geometry(root_geometry)
app = App(root)
root.mainloop()