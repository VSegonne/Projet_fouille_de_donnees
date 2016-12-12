from tkinter import *
from tkinter.ttk import *
import  tkinter.tix
from tkinter.messagebox import *
import random
import sys

class InitProfilPan(tkinter.Frame):

    def __init__(self, root, model):
        tkinter.Frame.__init__(self, root, width=600, height=700,  relief="groove")
        self.frameButton = Frame(self)
        self.count = 0
        self.recipes = model.getRecipes()
        print('LEN RECIPES', len(self.recipes))

        buttonFrame = ButtonFrame(self, model)
        self.recipeFrame = RecipeFrame(self, model)
        self.liked_recipes = []

        self.pack_propagate(False)

class ButtonFrame(Frame):

    def __init__(self, frame, model):
        Frame.__init__(self, frame, relief="ridge")
        self.root = frame
        iLikeButton = ILikeButton(self, model).grid(row=0, column=0)
        iDontLikeButton = IDontLikeButton(self, model).grid(row=0, column=1)
        nextButton = NextButton(self, model).grid(row=0, column=2)
        self.pack(side="bottom")

class ILikeButton(Button):

    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, self.frame, text="J'aime!", command=self.action)

    def action(self):
        if len(self.frame.root.liked_recipes) < 20:
            self.addRecipe2likedRecipes()
        else:
            self.model.generate_recipes()
            self.frame.root.destroy()

    def addRecipe2likedRecipes(self):

        self.frame.root.recipeFrame.destroy()
        self.frame.root.recipeFrame = RecipeFrame(self.frame.root, self.model)
        self.frame.root.liked_recipes.append(self.frame.root.recipes[0])
        self.frame.root.count += 1

class IDontLikeButton(Button):

    def __init__(self, frame, model):
        self.frame = frame
        Button.__init__(self, self.frame, text="Je n'aime pas!")
        #TODO
        # Add recipe to dont like

class NextButton(Button):

    def __init__(self, frame, model):
        self.frame = frame
        self.model =model
        Button.__init__(self, self.frame, text="Suivant", command=self.nextRecipe)

    def nextRecipe(self):
        self.frame.root.recipeFrame.destroy()

        self.frame.root.recipeFrame = RecipeFrame(self.frame.root, self.model)
        self.frame.root.count += 1


class RecipeFrame(Frame):

    def __init__(self, frame, model):
        Frame.__init__(self, frame)
        label = Label(self, text=frame.recipes[frame.count]["recipe_name"])
        label.pack()
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        frame.count += 1


