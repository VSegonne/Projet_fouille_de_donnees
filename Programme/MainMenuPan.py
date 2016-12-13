from tkinter import *
from tkinter.ttk import *
import  tkinter.tix
from tkinter.messagebox import *

class MainMenuPan(Frame):

    def __init__(self, root, DBM, model):
        Frame.__init__(self, root, width=400, height=200, relief="groove")
        self.DBM = DBM
        self.model = model
        self.okButton = OkButton(self, self.model)
        self.profile = ''
        self.entree = Entry(self, width = 30)
        self.entree.pack()

        self.listProfile = ListeProfile(self, self.model.getProfileNames())
        self.listProfile.pack()

        self.pack_propagate(False)

class OkButton(Button):
    def __init__(self, frame, model):
        self.model = model
        self.frame = frame

        Button.__init__(self, self.frame, text="Faire mon menu!",command=self.makeMenu)
        self.pack(side="bottom")

    def makeMenu(self):
        new_profile = self.frame.entree.get()

        # If no Profile chosen
        if new_profile == "" and self.frame.listProfile.get_profile_name() == "Choisissez votre profil":
            showerror("Attention!", "Vous devez choisir un profil", icon="warning")
            self.model.display_main_menu(self.model.root, self.model.DBM)

        # If new profile
        elif new_profile:
            if self.model.exists_profile(self.frame.entree.get()):
                res = askquestion("Attention!", "Ce profile existe déjà, voulez-vous le selectionner ?", icon="warning")
                if res == "yes":
                    sys.exit()
                else:
                    self.model.display_main_menu(self.model.root, self.model.DBM)
            else:
                showinfo('Bienvenu !', "C'est la première fois que vous utilisez ce programme. Avant de faire votre menu, je dois apprendre à vous connaitre! Pour cela, je vais vous présenter des recettes aléatoires, à vous de me dire si elle vous plaît. Lorsque vous aurez atteint 20 recettes  \
                         je vous proposerai un menu!")
                self.frame.destroy()
                self.model.init_cold_start(new_profile)
                #print(self.frame.entree.get())

        elif self.model.exists_profile(self.frame.listProfile.get_profile_name()):

            self.model.load_profile_from_database(self.frame.listProfile.get_profile_name())
            print(self.model.profile.get_liked_recipes())
            self.frame.destroy()
            self.model.generate_recipes()

            print("Connection succeeds!")


class ListeProfile(OptionMenu):

    def __init__(self, frame,  profileNames):
        self.profileVar = StringVar()
        OptionMenu.__init__(self, frame, self.profileVar, "Choisissez votre profil", *profileNames)


    def get_profile_name(self):
        return self.profileVar.get()


        self.pack()
