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

        suppButton =SuppRecipeButton(self, model)
        suppButton.grid(row=0, column=2)

        infoButton = InfoRecipeButton(self, model)
        infoButton.grid(row=1, sticky="W")


class AddRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Ajouter",command=self.add)

    def add(self):
        self.model.add_recipe_to_menu(self.frame.recipe)
        print(self.model.menu)



class SuppRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame =frame
        self.model =model
        Button.__init__(self, frame, text="Supprimer", command=self.sup)

    def sup(self):
        self.model.sup_recipe_from_menu(self.frame.recipe)
        print(self.model.menu)

class InfoRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Details", command=self.get_info)

    def get_info(self):
        recipe = self.frame.recipe
        text = "Type : " + recipe.get_type() + "\n\n"\
            + "Difficulté : " + recipe.get_difficulty() + "\n\n"\
            + "Coût : " + recipe.get_cost() + "\n\n" \
            + "Nb de couverts : " + recipe.get_guests_number() + "\n\n"\
            + "Temps de préparation : " + recipe.get_preparation_time() + "\n\n"\
            + "Temps de cuisson : " + recipe.get_cook_time() + "\n\n" \
            + "Ingredients : " + recipe.get_ingredients().replace('|',' ') + "\n\n"


        showinfo(self.frame.recipe.get_name(), text)



