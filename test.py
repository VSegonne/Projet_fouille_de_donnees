from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from scipy.spatial import distance
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from DataBaseManager import *
import operator
import sys
"""
corpus = ["mon premier document avec des voitures", \
          "mon deuxieme document avec des avions", \
          "Le dernier document avec des peintures", \
          "Ce document parle des avions"]


vectorizer = TfidfVectorizer(corpus)
X = vectorizer.fit_transform(corpus)
Y = vectorizer.get_feature_names()

kmeans = KMeans(n_clusters=3, verbose=1).fit(X.toarray()[:3])
print(kmeans.predict(X))

print(cosine_similarity(X))
"""

recipes = load_recipes_from_database("Recipes.db")
recipes_text = []
for recipe_dict in recipes:
    recipe_text = recipe_dict["recipe_name"] + " " + recipe_dict["ingredients"].replace(","," ") + " "+ recipe_dict["instructions"]
    recipes_text.append(recipe_text)

vectorizer = TfidfVectorizer(recipes_text)
X = vectorizer.fit_transform(recipes_text)
Y = vectorizer.fit_transform(recipes_text[101:])
kmeans = KMeans(n_clusters=15).fit(X)
recipe2test = X.toarray()[102:]

distance_totale = 0



unranked_cos_sim = []
unranked_min_dist = []
centers =[x for x in kmeans.cluster_centers_]


for i,recipe in enumerate(recipe2test):
   matrix = [recipe] + centers
   cos_matrix = cosine_similarity(matrix)
   euclyd = euclidean_distances(matrix)
   score_best_sim = max(cos_matrix[0][1:])
   score_min_dist = min(euclyd[0][1:])
   unranked_cos_sim.append((i,score_best_sim))
   unranked_min_dist.append(score_min_dist)

print(sum(unranked_min_dist)/len(unranked_min_dist))
sys.exit()

sorted_recipe = sorted(unranked_cos_sim,key=operator.itemgetter(1), reverse=True)
for i in range(7):
    print(recipes[sorted_recipe[i][0]]["recipe_name"])
sys.exit()
