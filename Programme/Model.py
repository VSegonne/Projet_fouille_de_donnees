import tkinter as tk
from MainMenuPan import *
from MakeMenuPan import *
from InitProfilPan import *
from Profile import *
from RecipeAdviser import  *
class Model():

    def __init__(self, root, DBM):
        print("ICI", root)
        self.DBM = DBM
        self.root = root
        self.profile = None
        self.recipes = self.DBM.load_recipes_from_database2(self.DBM.recipes_database)
        self.menu= []
        self.recommended_recipes =[]

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
        self.create_new_profile(profile_name)


        init = InitProfilPan(self.root, self)
        init.pack()


    def load_profile_from_database(self, profile_name):
        self.profile = self.DBM.load_profile_from_database(profile_name)

    def getRecipes(self):
        return self.DBM.load_recipes_from_database(self.DBM.database_file)


    def generate_recipes(self):

        self.recommended_recipes = self.get_recommended_recipes()
        print("Root", self.root)
        makeMenu = MakeMenuPan(self.root, self)
        makeMenu.pack()

    def get_recommended_recipes(self):
        recipeAdviser = RecipeAdviser(self.profile, self.recipes)
        return recipeAdviser.generate_recommended_recipes()


    def create_new_profile(self, profile_name):
        self.DBM.create_profile_table(profile_name)
        self.profile = Profile(profile_name)



    def add_liked_recipe_to_profile(self, profile_name, liked_recipe):
        liked_recipe.set_opinion("like")
        liked_recipe.set_score(1)
        self.profile.add_liked_recipe(liked_recipe)
        self.DBM.add_liked_recipe_to_profile(profile_name, liked_recipe)

    def add_disliked_recipe_to_profile(self, profile_name, disliked_recipe):
        disliked_recipe.set_opinion("dislike")
        self.profile.add_disliked_recipe(disliked_recipe)
        self.DBM.add_disliked_recipe_to_profile(profile_name, disliked_recipe)

    def add_recipe_to_menu(self, recipe):

        if recipe.get_opinion() != "like":
                showinfo('Attention', "Vous ne pouvez pas ajouter de recette que vous n'avez pas aimé..")

        if recipe.get_opinion() == "like":
            if len(self.menu) < 7 :
                self.menu.append(recipe)

            else:
                showinfo('Attention!', 'Vous avez déjà 7 repas!')

    def sup_recipe_from_menu(self, recipe):
        self.menu.remove(recipe)

    def increment_score_by_one(self, profile_name, recipe_name):
        self.DBM.increment_score_by_one(profile_name, recipe_name)
