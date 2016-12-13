from tkinter import *
from tkinter.ttk import *
import  tkinter.tix
from tkinter.messagebox import *
import random
import sys

class InitProfilPan(tkinter.Frame):

    def __init__(self, root, model):

        tkinter.Frame.__init__(self, root,  relief="groove")

        root.geometry("+220+150")

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
        if self.frame.root.count < 20 :
            self.frame.root.recipeNameFrame.update_name()
            self.frame.root.recipeFrame.update()
            self.addRecipe2likedRecipes()
        else:

            self.addRecipe2likedRecipes()
            self.frame.root.destroy()
            self.model.generate_recipes()

    def addRecipe2likedRecipes(self):

        profile_name = self.model.profile.get_name()
        liked_recipe = self.model.recipes[self.frame.root.count]
        liked_recipe.set_opinion("like")
        liked_recipe.set_score(1)
        self.model.add_liked_recipe_to_profile(profile_name, liked_recipe)


        # Destroy previous frame

        self.frame.root.recipeNameFrame.update_name()
        self.frame.root.recipeFrame.update()

        self.frame.root.count += 1


class IDontLikeButton(Button):

    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, self.frame, text="Je n'aime pas!", command=self.addRecipe2dislikedRecipes)


    def addRecipe2dislikedRecipes(self):


        profile_name = self.model.profile.get_name()
        disliked_recipe = self.model.recipes[self.frame.root.count]
        disliked_recipe.set_opinion("dislike")
        disliked_recipe.set_score(1)
        self.model.add_liked_recipe_to_profile(profile_name, disliked_recipe)

        self.frame.root.recipeNameFrame.update_name()
        self.frame.root.recipeFrame.update()

        self.frame.root.count += 1


class NextButton(Button):

    def __init__(self, frame, model):
        self.frame = frame
        self.model =model
        self.root = frame.root.root
        Button.__init__(self, self.frame, text="Suivant", command=self.nextRecipe)

    def nextRecipe(self):

        self.frame.root.count += 1

        # TODO
        # supprimer self.count+=1

        # Destroy previous frame
        self.frame.root.recipeNameFrame.update_name()
        self.frame.root.recipeFrame.update()

class RecipeNameFrame(LabelFrame):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        tkinter.LabelFrame.__init__(self, frame, text="Nom de la recette", relief="raised")
        self.label = tkinter.Label(self, text = frame.model.recipes[frame.count].get_name(), background="white")
        self.label.pack(padx=10, pady=10)
        self.grid(row=0, column=0, padx=15, pady=15)

    def update_name(self):
        #self.label.destroy()
        #self.label = tkinter.Label(self, text = self.model.recipes[self.frame.count].get_name(), background="white")
        #self.label.pack(padx=10, pady=10)
        self.label.configure(text = self.model.recipes[self.frame.count].get_name())

class RecipeDifficultyFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="difficulté", relief="raised")
        self.frame = frame
        self.model = model

        self.label = tkinter.Label(self, text = self.model.recipes[self.frame.root.count].get_difficulty(), background="white")
        self.label.pack(padx=5, pady=10)
        self.grid(row=1, column=0, padx=10, pady=10)

    def update_Difficulty(self):
        self.label.configure(text=self.model.recipes[self.frame.root.count].get_difficulty())
class RecipeCostFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Coût")
        self.frame = frame
        self.model = model
        self.label = tkinter.Label(self, text = self.model.recipes[self.frame.root.count].get_cost(), background="white")
        self.label.pack(padx=10, pady=10)
        self.grid(row=1, column=1, padx=10, pady=10)

    def update_Cost(self):
        self.label.configure(text = self.model.recipes[self.frame.root.count].get_cost())

class RecipeGuestsNbFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Nombre de couverts")
        self.frame = frame
        self.model = model

        self.label = tkinter.Label(self, text = self.model.recipes[self.frame.root.count].get_guests_number(), background="white")
        self.label.pack(padx=10, pady=10)
        self.grid(row=1, column=2, padx=10, pady=10)

    def update_Guests_number(self):
        self.label.configure(text = self.model.recipes[self.frame.root.count].get_guests_number())

class RecipePtimeFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Temps de Préparation")
        self.frame = frame
        self.model = model

        self.label = tkinter.Label(self, text = self.model.recipes[self.frame.root.count].get_preparation_time(), background="white")
        self.label.pack(padx=10, pady=10)
        self.grid(row=1, column=3, padx=10, pady=10)

    def update_Ptime(self):
        self.label.configure(text= self.model.recipes[self.frame.root.count].get_preparation_time()
                             )
class RecipeCtimeFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Temps de cuisson")
        self.frame = frame
        self.model = model

        self.label = tkinter.Label(self, text = frame.root.model.recipes[frame.root.count].get_cook_time(), background="white")
        self.label.pack(padx=10, pady=10)
        self.grid(row=1, column=4, padx=10, pady=10)

    def update_Ctime(self):
        self.label.configure(text= self.model.recipes[self.frame.root.count].get_cook_time())

class RecipeIngredientsFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Ingrédients")
        self.frame = frame
        self.model = model

        ingredients = ""
        for i, ingredient in enumerate(frame.root.model.recipes[frame.root.count].get_ingredients().split('|')):
            if i%5 == 0 :
                ingredients += "\n"
            else:
                ingredients += ingredient + ", "
        ingredients =ingredients.rstrip(', ')

        self.label = tkinter.Label(self, text = ingredients, background="white")
        self.label.pack(padx=10, pady=10)
        self.grid(row=3, column=1, padx=10, pady=10, columnspan=3)

    def update_Ingredients(self):
        ingredients = ""
        for i, ingredient in enumerate(self.model.recipes[self.frame.root.count].get_ingredients().split('|')):
            if i%5 == 0 :
                ingredients += "\n"
            else:
                ingredients += ingredient + ", "
        ingredients =ingredients.rstrip(', ')
        self.label.configure(text= ingredients)

class RecipeInstructionsFrame(LabelFrame):
    def __init__(self, frame, model):
        tkinter.LabelFrame.__init__(self, frame, text="Recette")
        instructions = ""
        self.frame = frame
        self.model = model
        for i, word in enumerate(frame.root.model.recipes[frame.root.count].get_instructions().split(" ")):
            if i%15 ==0:
                instructions += "\n"
            else:
                instructions += " "+ word

        self.label = tkinter.Label(self, text =instructions ,  background="white")
        self.label.pack(padx=10, pady=15)
        self.grid(row=4, column=1, padx=10, pady=10, columnspan=3)

    def update_Instructions(self):
        instructions = ""
        for i, word in enumerate(self.model.recipes[self.frame.root.count].get_instructions().split(" ")):
            if i%15 ==0:
                instructions += "\n"
            else:
                instructions += " "+ word

        self.label.configure(text = instructions)

class RecipeFrame(Frame):

    def __init__(self, root, model):
        tkinter.Frame.__init__(self, root)
        self.root = root
        self.model = model

        self.difficulty = RecipeDifficultyFrame(self, model)
        self.cost = RecipeCostFrame(self, model)
        self.guests_number = RecipeGuestsNbFrame(self, model)
        self.preparation_time = RecipePtimeFrame(self, model)
        self.cook_time = RecipeCtimeFrame(self, model)
        self.ingredients = RecipeIngredientsFrame(self, model)
        self.instructions = RecipeInstructionsFrame(self, model)

    def update(self):

        self.difficulty.update_Difficulty()

        self.cost.update_Cost()

        self.guests_number.update_Guests_number()

        self.preparation_time.update_Ptime()

        self.ingredients.update_Ingredients()

        self.cook_time.update_Ctime()

        self.instructions.update_Instructions()



