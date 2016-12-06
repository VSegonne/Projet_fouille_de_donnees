# -*- coding: utf-8 -*-

import sys
from DataBaseManager import *
from utils import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import operator
import random
from ProfileManager import *



#create_recipes_database_from_textFile("output_recipes_0512.txt")
#clean_database("Recipes.db", "Recipes")
#recipes = load_recipes_from_database("Recipes.db")

#vectorized_recipes = list(vectorize_recipes2(recipes).toarray())

#random.shuffle(recipes)

#liked_recipes =[]

#recipes_to_pop = []
#liked_count = 0

# PREMIER TEST
#for i, recipe in enumerate(recipes):
#    if recipe["type"] == "Plat principal":
#        print("\n")
#        print("Recette :",recipe["recipe_name"])
#        print("Ingrédients :",recipe["ingredients"])
#        print("Temps de préparation :",recipe["preparation_time"])
#        print("Temps de cuisson :",recipe["cook_time"])
#        res = input("Je valide ?\n")
#        if res == "y":
#            liked_count += 1
#            liked_recipes.append(vectorized_recipes[i])

 #           recipes_to_pop.append(i)
 #           vectorized_recipes.pop(i)
 #           recipes.pop(i)
#
#    print("Recipe numéro :",i)
#    print("Plats likés :", liked_count)

 #   if len(liked_recipes) == 20:
 #       break

#kmeans = KMeans(n_clusters=4).fit(liked_recipes)
#centers =[x for x in kmeans.cluster_centers_]


#unranked_cos_sim = []
#for i, recipe in enumerate(vectorized_recipes):
#    matrix = [recipe] + centers
#    cos_matrix = cosine_similarity(matrix)
#    score_best_sim = max(cos_matrix[0][1:])
#    unranked_cos_sim.append((i,score_best_sim))

#sorted_recipe = sorted(unranked_cos_sim,key=operator.itemgetter(1), reverse=True)
#print("=================================")
#print("\t propositions\n")

#for i in range(7):
#    print(recipes[sorted_recipe[i][0]]["recipe_name"],"\n")

#exists_profile("Recipes")
#create_profile_table("Vincent")
#liked_recipes = load_liked_recipes_from_profile("Vincent")
#print(liked_recipes)

print("\t=========================================")
print("\n\t\tBienvenu dans EatAWeek")
print("\n\t=========================================\n")

# Chargement et vectorization des recettes
recipes = load_recipes_from_database("Recipes.db")
v_recipes = vectorize_recipes2(recipes).toarray()


profile_name = input("Entrez votre nom : ")

# Si le profil existe déjà
if exists_profile(profile_name):
    print("\nUn profil correspond à votre nom ("+profile_name+")")
    print("Chargement de vos données ..")
    liked_recipes = load_liked_recipes_from_profile(profile_name)
    disliked_recipes = load_disliked_recipes_from_profile(profile_name)

    v_liked_recipes = vectorize_recipes2(liked_recipes)
    kmeans = KMeans(nb_cluster=10).fit(v_liked_recipes)
    centers =[x for x in kmeans.cluster_centers_]
else:
    print("Création de votre profil dans la base de donnée..\n")
    res = input("Appuyez sur n'importe quelle autre touche pour continuer")
    print("\nNous allons apprendre à vous connaitre! ")
    print("Pour cela nous allons vous présenter des recettes aléatoirement")
    print("Validez celles qui vous plaisent en appuyant sur la touche 'y', sur n'importe quelle autre touche sinon.")
    print("Lorsque vous aurez selectionné 20 recettes, nous vous ferons des recommandations!\n")
    res = input("Vous êtes prêt ? Appuyez sur n'importe quelle touche")
    print("\n\n========== CHOIX DES RECETTES ====================")

    liked_recipes = []
    liked_recipes_name = []
    v_liked_recipes = []
    liked_count = 0
    for i, recipe in enumerate(recipes):
      print("Vous avez aimé : " + str(liked_count) + " recettes")
      if recipe["type"] == "Plat principal":
        print("\n")
        print("Recette :",recipe["recipe_name"])
        print("Ingrédients :",recipe["ingredients"])
        print("Temps de préparation :",recipe["preparation_time"])
        print("Temps de cuisson :",recipe["cook_time"])
        res = input("Cette recette vous plaît (y) ?\n")
        if res == "y":
            liked_count += 1
            liked_recipes.append(recipe)
            liked_recipes_name.append(recipe["recipe_name"])
            v_liked_recipes.append(v_recipes[i])

        if len(liked_recipes) == 5:

            kmeans = KMeans(n_clusters=5).fit(v_liked_recipes)
            centers =[x for x in kmeans.cluster_centers_]
            unranked_cos_sim = []

            for i, recipe in enumerate(recipes):
                if recipe["recipe_name"] not in liked_recipes_name:
                    matrix = centers + v_recipes[i]
                    cos_matrix = cosine_similarity(matrix)
                    score_best_sim = max(cos_matrix[0][1:])
                    unranked_cos_sim.append((i,score_best_sim))
            sys.exit()
