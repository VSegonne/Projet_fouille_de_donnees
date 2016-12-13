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
    def __init__(self, root, model):
        Frame.__init__(self, root)
        self.root = root
        self.model = model

        Label(self, text = "CA MARCHE").pack()
        self.random_menu_frame = RandomMenuFrame(root, model)
        self.random_menu_frame.grid(row=0, column=0)


class BotFrame(Frame):
    def __init__(self, root, model):
        Frame.__init__(self, root)
        self.root = root
        self.model = model

class RandomMenuFrame(Frame):
    def __init__(self, frame, model):
        Frame.__init__(self, frame)
        self.frame = frame
        self.model = model

        self.random_recipes = random.sample(self.model.profile.get_liked_recipes(), len(self.model.profile.get_liked_recipes()))
        print(len(self.random_recipes))
        for i in range(7):
            recipe = RandomRecipeFrame(self, model, self.random_recipes[i])
            recipe.grid(row=i, padx=10, pady=10)

class RandomRecipeFrame(Frame):
    def __init__(self, frame, model, recipe):
        Frame.__init__(self, frame, relief="raised", width=400, height=140, borderwidth=2)
        self.frame = frame
        self.model = model
        self.recipe = recipe

        Label(self, text= recipe.get_name()).grid(row=0, column=0, sticky="W", padx=10, pady=10)

        self.grid_columnconfigure(0, minsize=400)

        addButton = AddRecipeButton(self, model)
        addButton.grid(row=0, column=1)

class AddRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, command=self.add)

    def add(self):
        self.model.add_recipe_to_menu(self.frame.recipe)
        print("MENU",self.model.menu)






