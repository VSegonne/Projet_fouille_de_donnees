# -*- coding: utf-8 -*-

import sys
import numpy as np
import sqlite3 as sq
import sys
from collections import defaultdict
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_recipe(recipe, ingredients, vocabulary, IDF):
    """ Return a vector built representing the recipe """

    # !!! http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html

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
        if ingredient in recipe["ingredients"].split('|'):
            vector[i] = 1
        else:
            vector[i] = 0

    # Vocabulary
    for word in vocabulary:
        i+=1
        vector[i] = getTF(recipe, word) * IDF[word]

    return vector


def recipes_to_term_documents(recipes):
    recipes_term_doc = []

    for recipe in recipes:
        recipe_text = recipe_dict["recipe_name"] + " " + recipe_dict["ingredients"].replace(","," ") + " "+ recipe_dict["instructions"]
        print(recipe_text)
        sys.exit()
        recipes_text.append(recipe_text)

    vectorizer = TfidfVectorizer(recipes_text)

    return vectorizer.fit_transform(recipes_text)


def vectorize_recipes2(recipes):

    # Difficulty

    # Get text from recipes
    recipes_text = []
    for recipe in recipes:
        recipe_text = recipe["recipe_name"] + " " \
            + recipe["ingredients"].replace("|", " ") + " " \
            + recipe["instructions"]

        recipes_text.append(recipe_text)

    # Vectorization using sklearn feature_extraction (text)
    vectorizer = TfidfVectorizer(recipes_text)
    recipes_term_document = vectorizer.fit_transform(recipes_text)

    return recipes_term_document


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

def getIngredients(recipes):
    """ Return a list containing an index of all ingredients found in the recipes """

    ingredients = set([])
    for recipe in recipes:
        for ingredient in recipe["ingredients"].split('|'):
            ingredients.add(ingredient)
    return ingredients

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

