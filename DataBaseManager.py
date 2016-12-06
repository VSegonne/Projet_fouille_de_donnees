# -*- coding: utf-8 -*-

import codecs
import sqlite3 as sq
import sys



def load_recipes_from_textFile(recipes_file):

    """ Load recipes from a text file"""

    database = open(recipes_file)
    #line = database.readline().decode("utf-8")
    line = database.readline()
    recipes = []
    recipe = {}

    recipes_name = set([]) #To avoid duplicates

    while line:

        if line == "\n":
            if recipe["type"] == "Plat principal" and recipe["recipe_name"] not in recipes_name:
                recipes_name.add(recipe["recipe_name"])
                recipes.append(recipe)
                recipe = {}

        else:
            line = line.rstrip()
            line = line.split('\t')
            print(line)
            recipe[line[0]] = line[1]

        #line = database.readline().decode("UTF-8")
        line = database.readline()
    database.close()
    return recipes




def create_recipes_database_from_textFile(database_name, recipes_file):

    recipes = load_recipes_from_textFile(recipes_file)

    conn = sq.connect()
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS Recipes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT,
                   recipe_name TEXT,
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


    for recipe in recipes:
        cursor.execute("""
                       INSERT INTO Recipes(url, recipe_name, type, difficulty, cost, guests_number, preparation_time, \
                       cook_time, ingredients, instructions) VALUES(:url, :recipe_name, :type, :difficulty, :cost, :guests_number, \
                      :preparation_time, :cook_time, :ingredients, :instructions)\
                       """, recipe
                        )



    conn.commit()
    conn.close()

def clean_database(database_file, table):

    """ Deletes duplicates in table """

    conn = sq.connect(database_file)
    cursor = conn.cursor()

    command = """ delete from """+table+""" where id not in (select  min(id) from """+table+""" group by recipe_name )"""
    cursor.execute(command)

    conn.commit()
    conn.close()

def load_recipes_from_database(database_file):

    conn = sq.connect(database_file)
    cursor = conn.cursor()

    col_names = ["url","recipe_name","type","difficulty","cost","guests_number", "preparation_time", "cook_time","ingredients","instructions" ]
    recipes = []

    for row in cursor.execute("SELECT * FROM Recipes"):
        recipe = {}
        for i, col in enumerate(row):
            if i > 0:
                recipe[col_names[i-1]] = col
        recipes.append(recipe)
    return recipes



# PROFILES MANAGEMENT

def exists_profile(profile_name):
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

def create_profile_table(profile_name):
    """ Create a table with the profile name
        Args :
                - profil_name : name of the profile
        Return : _
    """
    conn = sq.connect("Profile.db")
    cursor = conn.cursor()
    create = "CREATE TABLE " + profile_name + """(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              opinion TEXT,
              url TEXT,
              recipe_name TEXT,
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
    loading = "SELECT url, recipe_name, type, difficulty, cost, guests_number,\
        preparation_time, cook_time, ingredients, instructions FROM " + profile_name + \
        " WHERE opinion='like'"

    liked_recipes = []
    col_names = ["url","recipe_name", "type", "difficulty","cost", "guests_number",\
           "preparation_time", "cook_time", "ingredients", "instructions"]
    for row in cursor.execute(loading):
        #TODO CHANGER dict pour obj
        recipe = {}
        for i, col in enumerate(row):
            recipe[col_names[i]] = col
        liked_recipes.append(recipe)


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
    loading = "SELECT url, recipe_name, type, difficulty, cost, guests_number,\
        preparation_time, cook_time, ingredients, instructions FROM " + profile_name + \
        " WHERE opinion='dislike'"

    disliked_recipes = []
    col_names = ["url","recipe_name", "type", "difficulty","cost", "guests_number",\
           "preparation_time", "cook_time", "ingredients", "instructions"]
    for row in cursor.execute(loading):
        #TODO CHANGER dict pour obj
        recipe = {}
        for i, col in enumerate(row):
            recipe[col_names[i]] = col
        disliked_recipes.append(recipe)

    conn.close()
    return disliked_recipes


def add_liked_recipes_to_profile(profile_name, liked_recipes):
    #TODO Changer dict pour obj

    conn = sq.connect("Profile.db")
    cursor = conn.cursor()

    for recipe in liked_recipes:
        recipe["opinion"] = "like"
        #recipe_to_dump["opinion"] = "like"
        #recipe_to_dump["url"] = recipe["url"]
        #recipe_to_dump["recipe_name"] = recipe["recipe_name"]
        #recipe_to_dump["type"] = recipe["type"]
        #recipe_to_dump["difficulty"] = recipe["difficulty"]
        #recipe_to_dump["cost"] = recipe["cost"]
        #recipe_to_dump["guests_number"] = recipe["guests_number"]
        #recipe_to_dump["preparation_time"] = recipe["preparation_time"]
        #recipe_to_dump["cook_time"] = recipe["cook_time"]
        #recipe_to_dump["ingredients"] = recipe["ingredients"]
        #recipe_to_dump["instructions"] = recipe["instructions"]

        insert = """INSERT INTO """ + profile_name +"""
                (opinion, url, recipe_name, type, difficulty, cost, guests_number, preparation_time, cook_time,
                ingredients, instructions)
                values (:opinion, :url, :recipe_name, :type, :difficulty, :cost, :guests_number, :preparation_time,
                :cook_time, :ingredients, :instructions)
                """

        cursor.execute(insert, recipe)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    pass

