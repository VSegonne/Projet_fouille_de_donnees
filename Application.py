from DataBaseManager import *
from Model import *
import tkinter as tk


class Application():

    def __init__ (self, recipes_database_file, profiles_database_file):
        self.DBManager = DataBaseManager(recipes_database_file, profiles_database_file)


    def start(self):
        root = tk.Tk()
        root.title("EatAWeek")
        root.attributes("-topmost", True)
        root.geometry('500x300+350+400')
        model = Model(root, self.DBManager)
        model.display_main_menu(root, self.DBManager)
        root.mainloop()



