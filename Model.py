import tkinter as tk
from MainMenuPan import *
from InitProfilPan import *
class Model():

    def __init__(self, root, DBM):
        self.DBM = DBM
        self.root = root

    def display_main_menu(self, window, DBM):
        label = tk.Label(window, text="u piss me off")

        button1 = tk.Button(window, text="OK!")

        mainFrame = MainMenuPan(window, DBM, self)
        mainFrame.pack()


    def exists_profile(self,profile_name):
        return self.DBM.exists_profile(profile_name)


    def getProfileNames(self):
        return self.DBM.getProfileNames()

    def init_cold_start(self, profile_name):
        self.DBM.create_profile_table(profile_name)


        init = InitProfilPan(self.root, self)
        init.pack()

    def getRecipes(self):
        return self.DBM.load_recipes_from_database(self.DBM.database_file)


    def generate_recipes(self):
        print("Affichage des recettes proposées")
