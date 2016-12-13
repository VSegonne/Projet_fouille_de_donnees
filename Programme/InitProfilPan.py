from tkinter import *
from tkinter.ttk import *
import  tkinter.tix
from tkinter.messagebox import *
import random
import sys

class InitProfilPan(tkinter.Frame):

    def __init__(self, root, model):

        tkinter.Frame.__init__(self, root,  relief="groove")

        root.geometry("+250+150")

        self.root = root
        self.model = model
        self.count = 0


        self.recipeNameFrame = RecipeNameFrame(self, model)
        self.recipeNameFrame.grid(row= 0, column=0)

        self.recipeFrame = RecipeFrame(self, model)
        self.recipeFrame.grid(row=1, column=0, )

        self.buttonFrame = ButtonFrame(self, model).grid(row=3, column=0, pady=10)
        self.pack_propagate(False)

class ButtonFrame(Frame):

    def __init__(self, frame, model):
        Frame.__init__(self, frame, relief="ridge")
        self.root = frame
        iLikeButton = ILikeButton(self, model).grid(row=0, column=0)
        iDontLikeButton = IDontLikeButton(self, model).grid(row=0, column=1)
        nextButton = NextButton(self, model).grid(row=0, column=2)

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

        self.frame.root.Name.destroy()
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
        self.root = frame.root.root
        Button.__init__(self, self.frame, text="Suivant", command=self.nextRecipe)

    def nextRecipe(self):
        print("FUCKYOU")
        pass
        # Destroy previous frame
        #self.frame.root.recipeNameFrame.destroy()
        #self.frame.root.recipeFrame.destroy()


        #self.frame.root.recipeNameFrame = RecipeNameFrame(self.frame.root, self.model)
        #self.recipeNameFrame.grid(row= 0, column=0)

        #self.recipeFrame = RecipeFrame(self, self.model)
        #self.recipeFrame.grid(row=1, column=0, )
        #self.frame.root.count += 1


class RecipeNameFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Nom de la recette", relief="raised")
        tkinter.Label(self, text = frame.model.recipes[frame.count].get_name(), background="white").pack(padx=10, pady=10)
        self.grid(row=0, column=0, padx=15, pady=15)

class RecipeDifficultyFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="difficulté", relief="raised")
        frame.root.count += 1
        tkinter.Label(self, text = frame.root.model.recipes[frame.root.count].get_difficulty(), background="white").pack(padx=5, pady=10)
        self.grid(row=1, column=0, padx=10, pady=10)

class RecipeCostFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Coût")
        frame.root.count += 1
        tkinter.Label(self, text = frame.root.model.recipes[frame.root.count].get_cost(), background="white").pack(padx=10, pady=10)
        self.grid(row=1, column=1, padx=10, pady=10)

class RecipeGuestsNbFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Nombre de couverts")

        tkinter.Label(self, text = frame.root.model.recipes[frame.root.count].get_guests_number(), background="white").pack(padx=10, pady=10)
        self.grid(row=1, column=2, padx=10, pady=10)

class RecipePtimeFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Temps de Préparation")

        tkinter.Label(self, text = frame.root.model.recipes[frame.root.count].get_preparation_time(), background="white").pack(padx=10, pady=10)
        self.grid(row=1, column=3, padx=10, pady=10)

class RecipeCtimeFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Temps de cuisson")

        tkinter.Label(self, text = frame.root.model.recipes[frame.root.count].get_cook_time(), background="white").pack(padx=10, pady=10)
        self.grid(row=1, column=4, padx=10, pady=10)

class RecipeIngredientsFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Ingrédients")
        ingredients = ""
        for i, ingredient in enumerate(frame.root.model.recipes[frame.root.count].get_ingredients().split('|')):
            ingredients += ingredient + ", "
        ingredients =ingredients.rstrip(', ')

        tkinter.Label(self, text = ingredients, background="white").pack(padx=10, pady=10)
        self.grid(row=3, column=1, padx=10, pady=10, columnspan=3)

class RecipeInstructionsFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Recette")
        instructions = ""
        for i, word in enumerate(frame.root.model.recipes[frame.root.count].get_instructions().split(" ")):
            if i%15 ==0:
                instructions += "\n"
            else:
                instructions += " "+ word

        tkinter.Label(self, text =instructions ,  background="white").pack(padx=10, pady=15)
        self.grid(row=4, column=1, padx=10, pady=10, columnspan=3)

class RecipeFrame(Frame):

    def __init__(self, root, model):
        tkinter.Frame.__init__(self, root)
        self.root = root
        #name = RecipeNameFrame(self, model)
        difficulty = RecipeDifficultyFrame(self, model)
        cost = RecipeCostFrame(self, model)
        guests_number = RecipeGuestsNbFrame(self, model)
        preparation_time = RecipePtimeFrame(self, model)
        cook_time = RecipeCtimeFrame(self, model)
        ingredients = RecipeIngredientsFrame(self, model)
        instructions = RecipeInstructionsFrame(self, model)

