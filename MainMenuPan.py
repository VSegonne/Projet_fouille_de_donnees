from tkinter import *
from tkinter.ttk import *
import  tkinter.tix
from tkinter.messagebox import *

class MainMenuPan(Frame):

    def __init__(self, root, DBM, model):
        Frame.__init__(self, root, width=400, height=500, relief="groove")
        self.DBM = DBM
        self.model = model
        self.okButton = OkButton(self, self.model)
        self.pack_propagate(False)
        self.profile = ''
        self.entree = Entry(self, width = 30)
        self.entree.pack()
        self.profilevar = StringVar()

        self.profileNames = self.model.getProfileNames()
        self.listProfile = ListeProfile(self, self.profilevar, self.profileNames)
        self.listProfile.pack()


class OkButton(Button):
    def __init__(self, frame, model):
        self.model = model
        self.frame = frame

        Button.__init__(self, self.frame, text="Faire mon menu!",command=self.printOk)
        self.pack(side="bottom")

    def printOk(self):
        new_profile = self.frame.entree.get()
        if new_profile:
            showinfo('Bienvenu !', "C'est la première fois que vous utilisez ce programme")
            self.model.init_cold_start(new_profile)
            self.frame.destroy()
            #print(self.frame.entree.get())

        elif self.model.exists_profile(self.frame.v.get()):
            print("Connection succeeds!")


class ListeProfile(OptionMenu):

    def __init__(self, frame, profilevar, profileNames):
        OptionMenu.__init__(self, frame, profilevar, "Choisissez votre profile", *profileNames)




        self.pack()
