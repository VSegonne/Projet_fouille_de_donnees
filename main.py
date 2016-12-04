# -*- coding: utf-8 -*-

import sys
from DataBaseManager import *
from utils import *


recipes = load_recipes_from_database("Recipes.db")

vectorized_recipes = []
ingredients = getIngredients(recipes)
vocabulary = getVocabulary(recipes)
IDF = getIDF(recipes)
for recipe in recipes:
    vectorized_recipes.append(vectorize_recipe(recipe, ingredients, vocabulary, IDF))

for element in vectorized_recipes:
    print(element)

print(len(vectorized_recipes))
