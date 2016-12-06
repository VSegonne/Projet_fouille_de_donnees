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




#=========================================================
#           Script de tests préliminaires
#=========================================================


print("\t=========================================")
print("\n\t\tBienvenu dans EatAWeek")
print("\n\t=========================================\n")

# Chargement et vectorization des recettes
recipes = load_recipes_from_database("Recipes.db")
v_recipes = vectorize_recipes2(recipes).toarray()

# Demande du nom de l'utilisateur
profile_name = input("Entrez votre nom : ")

# Si le profil existe déjà
if exists_profile(profile_name):
    print("\nUn profil correspond à votre nom ("+profile_name+")")
    print("Chargement de vos données ..")
    res = input("Appuyez sur n'importe quelle touche pour continuer")

    # Chargement des données du profil de l'utilisateur (liked + disliked recipes)
    liked_recipes = load_liked_recipes_from_profile(profile_name)
    liked_recipes_names = [liked_recipes[x]["recipe_name"] for x in range(len(liked_recipes))]
    disliked_recipes = load_disliked_recipes_from_profile(profile_name)

    # Vectorisation des recettes likées par l'utilisateur
    v_liked_recipes = [v_recipes[x] for x in range(len(recipes)) if recipes[x]["recipe_name"] in liked_recipes_names]

    # Représentation du profil via clustering (kmeans)
    kmeans = KMeans(n_clusters=5).fit(v_liked_recipes)
    centers =[x for x in kmeans.cluster_centers_]


    unranked_cos_sim = []

    # On trie les similarités pour avoir les meilleurs au début de la liste

    # Phase de recommandation
    for i, recipe in enumerate(recipes):
        if recipe["recipe_name"] not in liked_recipes_names:
            matrix = centers + v_recipes[i]
            cos_matrix = cosine_similarity(matrix)
            score_best_sim = max(cos_matrix[0][1:])
            unranked_cos_sim.append((i,score_best_sim))

    sorted_recommendation = sorted(unranked_cos_sim,key=operator.itemgetter(1), reverse=True)
    print("\n---------------------------------------")
    print("\tRecommandations\n")
    print("Voici 7 repas que nous avons choisi pour vous")
    print("Vous pouvez les valider en tapant 'y', ils seront alors rajouter à votre profil")
    print("ce qui nous permettra de mieux vous recommander des nouvelles recettes\n")
    res = input("Appuyez sur n'importe quelle touche pour continuer")

    newly_liked = []
    for i, element in enumerate(sorted_recommendation[:7]):
                print("\n")

                print(recipes[element[0]]["recipe_name"])
                print("Ingrédients :",recipes[element[0]]["ingredients"])
                print("Temps de préparation :",recipes[element[0]]["preparation_time"])
                print("Temps de cuisson :",recipes[element[0]]["cook_time"])
                res = input("Est-ce que cette recette vous plaît ? (y)\n")
                if res == 'y':
                    liked_recipes.append(recipes[element[0]])
                    newly_liked.append(recipes[element[0]])

    add_liked_recipes_to_profile(profile_name, newly_liked)
    clean_database("Profile.db",profile_name)

    print("Les recettes que vous avez liké ont bien été ajoutées!")

    print("\t==================================")
    print("\tMerci c'est terminé ! À bientôt ")
    print("\t==================================")

# Si le profil n'existe pas on lance la phase d'initialisation d'un nouveau profil
else:

    # Création du profil dans la base de donnée
    create_profile_table(profile_name)

    print("Vous êtes nouveau :) ")
    print("Création de votre profil dans la base de donnée..\n")
    res = input("Appuyez sur n'importe quelle autre touche pour continuer")
    print("\nNous allons apprendre à vous connaitre! ")
    print("Pour cela nous allons vous présenter des recettes aléatoirement")
    print("Validez celles qui vous plaisent en appuyant sur la touche 'y', sur n'importe quelle autre touche sinon.")
    print("Lorsque vous aurez selectionné 20 recettes, nous vous ferons des recommandations!\n")
    res = input("Vous êtes prêt ? Appuyez sur n'importe quelle touche")
    print("\n\n========== CHOIX DES RECETTES ====================")

    # Apprentissage des goûts de l'utilisateur


    recipes = random.shuffle(recipes)

    # Les recettes qu'il va aimer
    liked_recipes = []

    # Le nom des recettes qu'il va aimer (sert plus tard)
    liked_recipes_name = []

    # La version vectorisée des recettes qu'il va aimer
    v_liked_recipes = []

    # Compteur pour savoir combien de recettes il reste à liker
    liked_count = 0

    # On boucle sur tous les repas jusqu'à ce que l'utilisateur ait liké 20 repas
    for i, recipe in enumerate(recipes):

      print("Vous avez aimé : " + str(liked_count) + " recettes")
      if recipe["type"] == "Plat principal":
        print("\n")
        print("Recette :",recipe["recipe_name"])
        print("Ingrédients :",recipe["ingredients"])
        print("Temps de préparation :",recipe["preparation_time"])
        print("Temps de cuisson :",recipe["cook_time"])
        res = input("Cette recette vous plaît (y) ?\n")

        # Validation de la recette
        if res == "y":
            liked_count += 1
            liked_recipes.append(recipe)
            liked_recipes_name.append(recipe["recipe_name"])
            v_liked_recipes.append(v_recipes[i])

        # Si 20 recettes ont été likée on lance la phase de recommandation
        if len(liked_recipes) == 5:
            kmeans = KMeans(n_clusters=5).fit(v_liked_recipes)
            centers =[x for x in kmeans.cluster_centers_]
            unranked_cos_sim = []

            # Phase de recommandation
            for i, recipe in enumerate(recipes):
                if recipe["recipe_name"] not in liked_recipes_name:
                    matrix = centers + v_recipes[i]
                    cos_matrix = cosine_similarity(matrix)
                    score_best_sim = max(cos_matrix[0][1:])
                    unranked_cos_sim.append((i,score_best_sim))

            # On trie les similarités pour avoir les meilleurs au début de la liste
            sorted_recommendation = sorted(unranked_cos_sim,key=operator.itemgetter(1), reverse=True)

            # Phase de validation des recommandations
            print("\n==================================================================")
            print("\nMerci! Vous avez bien selectionné 20 recettes\n")
            res = input("Appuyez sur n'importe quelle touche pour continuer")
            print("\n---------------------------------------")
            print("\tRecommandations\n")
            print("Voici 7 repas que nous avons choisi pour vous")
            print("Vous pouvez les valider en tapant 'y', ils seront alors rajouter à votre profil")
            print("ce qui nous permettra de mieux vous recommander des nouvelles recettes\n")
            res = input("Appuyez sur n'importe quelle touche pour continuer")


            for i, element in enumerate(sorted_recommendation[:7]):
                print("\n")

                print(recipes[element[0]]["recipe_name"])
                print("Ingrédients :",recipes[element[0]]["ingredients"])
                print("Temps de préparation :",recipes[element[0]]["preparation_time"])
                print("Temps de cuisson :",recipes[element[0]]["cook_time"])
                res = input("Est-ce que cette recette vous plaît ? (y)\n")
                if res == 'y':
                    liked_recipes.append(recipes[i])


            add_liked_recipes_to_profile(profile_name, liked_recipes)
            clean_database("Profile.db",profile_name)

            print("Les recettes que vous avez liké ont bien été ajoutées!")
            print("\t==================================")
            print("\tMerci c'est terminé ! À bientôt ")
            print("\t==================================")
            sys.exit()
