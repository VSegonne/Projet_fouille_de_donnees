# -*- coding: utf-8 -*-

import sys
from DataBaseManager import *
from utils import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import operator

#create_recipes_database_from_textFile("output_recipes_0312.txt")
clean_database("Recipes.db", "Recipes")
recipes = load_recipes_from_database("Recipes.db")
print(len(recipes))
vectorized_recipes = list(vectorize_recipes2(recipes).toarray())
print(type(vectorized_recipes))

liked_recipes =[]

recipes_to_pop = []

for i, recipe in enumerate(recipes):
    if recipe["type"] == "Plat principal":
        print("\n",recipe["recipe_name"])
        print(recipe["ingredients"])
        print(recipe["preparation_time"])
        print(recipe["cook_time"])
        res = input("Je valide ?\n")
        if res == "y":
            liked_recipes.append(vectorized_recipes[i])

            recipes_to_pop.append(i)
            vectorized_recipes.pop(i)
            recipes.pop(i)
            print("LEn RECIPES",len(recipes))
            print("LEn VECTOR RECIPES",len(vectorized_recipes))

    if len(liked_recipes) == 20:
        break

kmeans = KMeans(n_clusters=4).fit(liked_recipes)
centers =[x for x in kmeans.cluster_centers_]


unranked_cos_sim = []
for i, recipe in enumerate(vectorized_recipes):
    matrix = [recipe] + centers
    cos_matrix = cosine_similarity(matrix)
    score_best_sim = max(cos_matrix[0][1:])
    unranked_cos_sim.append((i,score_best_sim))

print("HEYYY")
sorted_recipe = sorted(unranked_cos_sim,key=operator.itemgetter(1), reverse=True)
for i in range(7):
    print(recipes[sorted_recipe[i][0]]["recipe_name"])
