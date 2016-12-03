import sqlite3 as sq
import sys
from collections import defaultdict
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
"""
                    -- EatAWeek project --
                    De Zaho / Vincent Segonne

    Program to create sqlite database containing recipes
    Recipes are extracted from marmiton.org using recipes.php
    Input : STDIN
    Output : recipes.db

"""


def load_recipes_from_textFile(recipes_file):

    """ Load recipes from a text file"""

    database = open(recipes_file)
    line = database.readline()
    recipes = []
    recipe = {}

    recipes_name = set([]) #To avoid doubles

    while line:

        if line == "\n":
            if recipe["type"] == "Plat principal" and recipe["recipe_name"] not in recipes_name:
                recipes_name.add(recipe["recipe_name"])
                recipes.append(recipe)
                recipe = {}

        else:
            line = line.rstrip()
            line = line.split('\t')

            if line[0] == "ingredient":
                recipe[line[0]] = line[1].replace(',','|')
            recipe[line[0]] = line[1]

        line = database.readline()
    database.close()
    return recipes


def getIngredients(recipes):
    """ Return a list containing an index of all ingredients found in the recipes """

    ingredients = set([])
    for recipe in recipes:
        for ingredient in recipe["ingredient"].split('|'):
            ingredients.add(ingredient)
    return ingredients

def getVocabulary(recipes):
    """ Return a list of words found in all recipes' instructions and title """

    # irrelvant words
    STOP_WORDS = ["elle", "Elle", "il", "Il", "de", "avec","Avec", "pour", "Pour", "jusqu'à","Jusqu'à",\
                  "pendant", "Pendant",  "au", "Au","au", "et", "à","À",  "le","Le", "La", \
                  "la", "les","Les", "ces","Ces", "ce","Ce", "un","Un", "une", "des",\
                  "en","En", "vous", "Vous", "même","Même","y", "Y","ce", "Ce", "lorsqu'elle"   \
                  "ou", "puis", "Puis", "ensuite","Ensuite", "dans", "bien", "du", "vos", "peu",\
                  "Lorsqu'elle", "lorsqu'il", "Lorsqu'il", "que","qui", "sur", "quelques", "quand", "Quand",\
                  "tout", "Tout", "toute", "Toute", "Toutes", "!", "?", ".", "..", "...", ",", \
                  "ça", "1", "2", "3", '4', "4", "5", "6", "7", "8", "9", "10", "dl", "cl","ml","kg", \
                  "gr","cm",  "",'', "+", "ca", "ne", "°c", "°C", "cela", "Cela", "g", "ceux", "a", \
                  "votre","ou","son","enfin", "Enfin", "quant", "maxi", "si", "par", "on", "ses",\
                  "alors","très", "dessus", "autour","mn", "dés", "toutes", "toute", "tout", "afin", "minute",\
                  "min", ";", ":", "th"]

    PARASITE = [",", ".", "..","...","....", "'", "\"", "/", "\\", "!", "(", ")", "-", "'","_", ";", "+"]
    NUMBERS = ["0", "1", "2", "3", '4', "4", "5", "6", "7", "8", "9"]
    vocabulary = set([])

    for recipe in recipes:
        # Words in recipe name
        for word in recipe["recipe_name"].split(" "):
            clean = True
            for parasite in PARASITE:
                if parasite in word:
                    clean = False
            for number in NUMBERS:
                if number in word:
                    clean = False
            if word.lower() not in STOP_WORDS and clean == True:
                vocabulary.add(word)

        # Words in recipe instructions
        for word in recipe["instructions"].split(" "):
            clean = True
            for parasite in PARASITE:
                if parasite in word:
                    clean = False
            for number in NUMBERS:
                if number in word:
                    clean = False
            if word.lower() not in STOP_WORDS and clean == True:
                vocabulary.add(word)

    return vocabulary

def getIDF(recipes):

    vocabulary = getVocabulary(recipes)
    idf = defaultdict(float)

    for word in vocabulary:
        for recipe in recipes:
            if word in recipe["recipe_name"] or word in recipe["instructions"]:
                idf[word] += 1

    for word in vocabulary:
        idf[word] = math.log(len(recipes)/idf[word])

    return idf

def getTF(recipe, word):

    TF = 0

    for word2 in recipe["recipe_name"].split(" "):
        if word == word2:
            TF+=1

    for word2 in recipe["instructions"].split(" "):
        if word == word2:
            TF+=1

    return TF


def vectorize_recipe(recipe, ingredients, vocabulary, IDF):
    """ Return a vector built representing the recipe """

    vector = [0] * (12+ len(ingredients) + len(vocabulary))
    i = 0

    # Difficulty
    difficulty = ["Facile", "Moyen", "Difficile"]
    for dif in difficulty:
        i+=1
        if recipe["difficulty"] == dif:
            vector[i] = 1
        else:
            vector[i] = 0

    # Cost
    cost = ["Bon marché", "cher"]
    for price in cost:
        i+=1
        if recipe["cost"] == price:
            vector[i] = 1
        else:
            vector[i] = 0

    # Cook Time
    if int(recipe["cook_time"]) in range(0,15):
        i+=1
        vector[i] = 1
    else:
        i+=1
        vector[i] = 0

    if int(recipe["cook_time"]) in range(15,30):
        i+=1
        vector[i] = 1
    else:
        i+=1
        vector[i] = 0

    if int(recipe["cook_time"]) > 30:
        i+=1
        vector[i]= 1
    else:
        i+=1
        vector[i] = 0

    # Preparation Time
    if int(recipe["preparation_time"]) in range(0,10):
        i+=1
        vector[i] = 1
    else:
        i+=1
        vector[i] = 0

    if int(recipe["preparation_time"]) in range(10,30):
        i+=1
        vector[i] = 1
    else:
        i+=1
        vector[i] = 0

    if int(recipe["preparation_time"]) > 30:
        i+=1
        vector[i]= 1
    else:
        i+=1
        vector[i] = 0

    # Ingredients
    for ingredient in ingredients:
        i+=1
        if ingredient in recipe["ingredient"]:
            vector[i] = 1
        else:
            vector[i] = 0

    # Vocabulary
    for word in vocabulary:
        i+=1
        vector[i] = getTF(recipe, word) * IDF[word]

    return vector

def createDatabase(recipes):

    conn = sq.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS Recipes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT,
                   name TEXT,
                   type TEXT,
                   difficulty TEXT,
                   cost TEXT,
                   guest_number TEXT,
                   preparation_time TEXT,
                   cook_time TEXT,
                   instructions TEXT
                )
                   """
                   )

    for recipe in recipes:
        cursor.execute("""
                       INSERT INTO Recipes(url, name, type, difficulty, cost, guests_number, preparation_time, \
                       cook_time, instructions) VALUES(:url, :name, :type, :difficulty, :cost, :guest_number, \
                       :preparation_time, :cook_time, :instructions)\
                       """, recipe
                        )

    conn.commit()


    conn.close()


def showDatabase():

    conn = sq.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute(""" SELECT ID,NAME,INGREDIENTS FROM Recipes""")
    recipe1 = cursor.fetchone()
    print(len(recipe1))

    print(recipe1)

if __name__ == "__main__":

    #createDatabase()
    #showDatabase()
    recipes = load_recipes_from_textFile("output_recipes_0212.txt")
    ingredients = getIngredients(recipes)
    vocabulary = getVocabulary(recipes)
    IDF = getIDF(recipes)
    vector1 = np.array(vectorize_recipe(recipes[0], ingredients, vocabulary, IDF))
    vector2 = np.array(vectorize_recipe(recipes[3], ingredients, vocabulary, IDF))
    A = np.array(vector1)
    B = np.array(vector2)
    matrix = np.array([vector1,vector2])

