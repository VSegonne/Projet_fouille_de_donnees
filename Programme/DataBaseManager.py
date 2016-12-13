# -*- coding: utf-8 -*-

import sqlite3 as sq
import sys
#import chardet
from Recipe import  *
from Profile import *

class DataBaseManager():

    def __init__(self, recipes_database=None, profiles_database=None) :
        self.recipes_database = recipes_database
        self.profiles_database = profiles_database

    def load_recipes_from_textFile(self, recipes_file) :

        """ Load recipes from a text file"""

        database = open(recipes_file)
        #line = database.readline().decode("utf-8")
        line = database.readline()
        recipes = []
        recipe = {}

        recipes_name = set([]) #To avoid duplicates

        while line:
            if line == "\n" :
                if recipe["type"] == "Plat principal" and recipe["name"] not in recipes_name :
                    recipes_name.add(recipe["name"])
                    recipes.append(recipe)
                    recipe = {}
            else :
                line = line.rstrip()
                line = line.split('\t')
                if line[0] == "recipe_name":
                    recipe["name"] = line[1]
                recipe[line[0]] = line[1]

            #line = database.readline().decode("UTF-8")
            line = database.readline()

        database.close()
        return recipes

    def create_recipes_database_from_textFile(self, database_name, recipes_file) :

        recipes = self.load_recipes_from_textFile(recipes_file)

        conn = sq.connect(database_name)
        conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        cursor = conn.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Recipes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    name TEXT,
                    type TEXT,
                    difficulty TEXT,
                    cost TEXT,
                    guests_number TEXT,
                    preparation_time TEXT,
                    cook_time TEXT,
                    ingredients TEXT,
                    instructions TEXT
                    )
                    """
                    )

        for recipe in recipes :
            cursor.execute("""
                        INSERT INTO Recipes(url, name, type, difficulty, cost, guests_number, preparation_time, \
                        cook_time, ingredients, instructions) VALUES(:url, :name, :type, :difficulty, :cost, :guests_number, \
                        :preparation_time, :cook_time, :ingredients, :instructions)\
                        """, recipe
                            )

        conn.commit()
        conn.close()

    def clean_database(self, database_file, table):

        """ Deletes duplicates in table """

        conn = sq.connect(database_file)
        cursor = conn.cursor()

        command = """ delete from """+table+""" where id not in (select  min(id) from """+table+""" group by name )"""
        cursor.execute(command)

        conn.commit()
        conn.close()

    def load_recipes_from_database(self, database_file):

        conn = sq.connect(database_file)
        cursor = conn.cursor()

        col_names = ["url","name","type","difficulty","cost","guests_number", "preparation_time", "cook_time","ingredients","instructions" ]
        recipes = []

        for row in cursor.execute("SELECT * FROM Recipes"):

            recipe = {}
            for i, col in enumerate(row):
                if i > 0:
                    recipe[col_names[i-1]] = col

            recipes.append(recipe)
        return recipes

    def load_recipes_from_database2(self, database_file):

        conn = sq.connect(database_file)
        cursor = conn.cursor()

        recipes = []

        for row in cursor.execute("SELECT * FROM Recipes"):
            recipe_attributes = []
            for i, col in enumerate(row):
                if i > 0:
                    recipe_attributes.append(col)

            recipe = Recipe(*recipe_attributes)
            recipes.append(recipe)
        return recipes


    # PROFILES MANAGEMENT

    def exists_profile(self, profile_name):
        """ Check if a a table with the profile name exists in Profile.db
            Args :
                    - profile_name : name of the profile : str
            Return:
                    - Bool
        """


        conn = sq.connect("Profile.db")

        cursor = conn.cursor()
        exists = "SELECT * FROM sqlite_master WHERE type='table' and name='"+profile_name+"'"
        if cursor.execute(exists).fetchone():
            conn.close()
            return True
        else:
            conn.close()
            return False

    def create_profile_table(self, profile_name):
        """ Create a table with the profile name
            Args :
                    - profil_name : name of the profile
            Return : _
        """
        conn = sq.connect("Profile.db")
        conn.text_factory = str
        cursor = conn.cursor()
        create = "CREATE TABLE " + profile_name + """(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                name TEXT,
                type TEXT,
                difficulty TEXT,
                cost TEXT,
                guests_number TEXT,
                preparation_time TEXT,
                cook_time TEXT,
                ingredients TEXT,
                instructions TEXT,
                opinion TEXT,
                score TEXT
                )
                """
        cursor.execute(create)
        conn.commit()
        conn.close()

    def load_liked_recipes_from_profile(profile_name):
        """ Load the recipes that have been liked by the profile user
            Args:
                    - profile_name : the profile name : str
            Return:
                    - Recipe (obj)
        """
        conn = sq.connect("Profile.db")
        cursor = conn.cursor()
        loading = "SELECT url, name, type, difficulty, cost, guests_number,\
            preparation_time, cook_time, ingredients, instructions FROM " + profile_name + \
            " WHERE opinion='like'"

        liked_recipes = []
        col_names = ["url","name", "type", "difficulty","cost", "guests_number",\
            "preparation_time", "cook_time", "ingredients", "instructions"]
        for row in cursor.execute(loading):
            #TODO CHANGER dict pour obj
            recipe = {}
            for i, col in enumerate(row):
                recipe[col_names[i]] = col
            liked_recipes.append(recipe)


        conn.close()
        return liked_recipes

    def load_liked_recipes_from_profile2(self, profile_name):
        """ Load the recipes that have been liked by the profile user
            Args:
                    - profile_name : the profile name : str
            Return:
                    - Recipe (obj)
        """
        conn = sq.connect("Profile.db")
        cursor = conn.cursor()
        loading = "SELECT url, name, type, difficulty, cost, guests_number,\
            preparation_time, cook_time, ingredients, instructions, opinion, score FROM " + profile_name + \
            " WHERE opinion='like'"

        liked_recipes = []

        for row in cursor.execute(loading):
            recipe_attributes = []
            for i, col in enumerate(row):
                recipe_attributes.append(col)
            liked_recipe = Recipe(*recipe_attributes)
            liked_recipe.set_opinion("like")
            liked_recipes.append(liked_recipe)


        conn.close()
        return liked_recipes

    def load_disliked_recipes_from_profile2(self, profile_name):
        """ Load the recipes that have been liked by the profile user
            Args:
                    - profile_name : the profile name : str
            Return:
                    - Recipe (obj)
        """
        conn = sq.connect("Profile.db")
        cursor = conn.cursor()
        loading = "SELECT url, name, type, difficulty, cost, guests_number,\
            preparation_time, cook_time, ingredients, instructions, opinion, score FROM " + profile_name + \
            " WHERE opinion='dislike'"

        liked_recipes = []

        for row in cursor.execute(loading):
            recipe_attributes = []
            for i, col in enumerate(row):
                recipe_attributes.append(col)
            liked_reciped = Recipe(*recipe_attributes)
            liked_reciped.set_opinion("like")
            liked_recipes.append(liked_recipe)


        conn.close()
        return liked_recipes

    def load_disliked_recipes_from_profile(profile_name):
        """ Load the recipes that have been liked by the profile user
            Args:
                    - profile_name : the profile name : str
            Return:
                    - Recipe (obj)
        """
        conn = sq.connect("Profile.db")
        cursor = conn.cursor()
        loading = "SELECT url, name, type, difficulty, cost, guests_number,\
            preparation_time, cook_time, ingredients, instructions FROM " + profile_name + \
            " WHERE opinion='dislike'"

        disliked_recipes = []
        col_names = ["url","name", "type", "difficulty","cost", "guests_number",\
            "preparation_time", "cook_time", "ingredients", "instructions"]
        for row in cursor.execute(loading):
            #TODO CHANGER dict pour obj
            recipe = {}
            for i, col in enumerate(row):
                recipe[col_names[i]] = col
            disliked_recipes.append(recipe)

        conn.close()
        return disliked_recipes


    def add_liked_recipes_to_profile(self, profile_name, liked_recipes):

        conn = sq.connect("Profile.db")
        cursor = conn.cursor()

        for recipe in liked_recipes:
            recipe = self.recipe2dict(recipe)

            insert = """INSERT INTO """ + profile_name +"""
                    (url, name, type, difficulty, cost, guests_number, preparation_time, cook_time,
                    ingredients, instructions, opinion, score)
                    values (:url, :name, :type, :difficulty, :cost, :guests_number, :preparation_time,
                    :cook_time, :ingredients, :instructions, :opinion, :score)
                    """

            cursor.execute(insert, recipe)

        conn.commit()
        conn.close()

    def add_liked_recipe_to_profile(self, profile_name, liked_recipe):

        conn = sq.connect("Profile.db")
        cursor = conn.cursor()

        recipe = self.recipe2dict(liked_recipe)

        insert = """INSERT INTO """ + profile_name +"""
                    (url, name, type, difficulty, cost, guests_number, preparation_time, cook_time,
                    ingredients, instructions, opinion, score)
                    values (:url, :name, :type, :difficulty, :cost, :guests_number, :preparation_time,
                    :cook_time, :ingredients, :instructions, :opinion, :score)
                    """

        cursor.execute(insert, recipe)

        conn.commit()
        conn.close()

    def add_disliked_recipe_to_profile(self, profile_name, disliked_recipe):

        conn = sq.connect("Profile.db")
        cursor = conn.cursor()

        recipe = self.recipe2dict(disliked_recipe)

        insert = """INSERT INTO """ + profile_name +"""
                    (url, name, type, difficulty, cost, guests_number, preparation_time, cook_time,
                    ingredients, instructions, opinion, score)
                    values (:url, :name, :type, :difficulty, :cost, :guests_number, :preparation_time,
                    :cook_time, :ingredients, :instructions, :opinion, :score)
                    """

        cursor.execute(insert, recipe)

        conn.commit()
        conn.close()

    def recipe2dict(self, recipe):
        recipe_dict = {}
        recipe_dict["url"] = recipe.get_url()
        recipe_dict["name"] = recipe.get_name()
        recipe_dict["type"] = recipe.get_type()
        recipe_dict["difficulty"] = recipe.get_difficulty()
        recipe_dict["cost"] = recipe.get_cost()
        recipe_dict["guests_number"] = recipe.get_guests_number()
        recipe_dict["preparation_time"] = recipe.get_preparation_time()
        recipe_dict["cook_time"] = recipe.get_cook_time()
        recipe_dict["ingredients"] = recipe.get_ingredients()
        recipe_dict["instructions"] = recipe.get_instructions()
        recipe_dict["opinion"] = recipe.get_opinion()
        recipe_dict["score"] = recipe.get_score()

        return recipe_dict

    def getProfileNames(database_file):
        conn = sq.connect("Profile.db")
        cursor = conn.cursor()
        command = """ select  name from  sqlite_master  where type='table' """
        names = []
        for name in cursor.execute(command):
            if name[0] != "sqlite_sequence":
                names.append(name[0])
        return names


    def load_profile_from_database(self, profile_name):

        profile = Profile(profile_name)


        liked_profile = self.load_liked_recipes_from_profile2(profile_name)
        profile.set_liked_recipes(liked_profile)

        disliked_profile = self.load_disliked_recipes_from_profile2(profile_name)
        profile.set_disliked_recipes(disliked_profile)

        return profile

if __name__ == "__main__":
    newDB = DataBaseManager()
    newDB.create_recipes_database_from_textFile("Recipes3.db","recipes_index_B.txt")
    newDB.clean_database("Recipes3.db","Recipes")
