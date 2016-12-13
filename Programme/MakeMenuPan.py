from tkinter import *
from tkinter.messagebox import *
import random
import sys

class MakeMenuPan(Frame):

    def __init__(self, root, model):
        Frame.__init__(self, root)
        self.root = root
        self.model = model


        self.topFrame = TopFrame(self, model)
        self.topFrame.grid(row=0)

        self.botFrame = BotFrame(self, model)
        self.botFrame.grid(row=0)

        self.pack_propagate(False)



class TopFrame(Frame):
    def __init__(self, frame, model):
        Frame.__init__(self, frame)

        Label(self, text = "CA MARCHE").pack()


class BotFrame(Frame):
    def __init__(self, frame, model):
        Frame.__init__(self, frame)

class RandomMenuFrame(Frame):
    def __init__(self, frame, model):
        Frame.__init__(self, frame)
