from utils import  *
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RecipeAdviser():
    def __init__(self, profile, recipes):
        self.profile = profile
        self.recipes= recipes


    def generate_recommended_recipes(self):
        v_recipes = vectorize_recipes2(self.recipes)
        liked_recipes = [x for x in self.profile.get_liked_recipes()]
        liked_recipes_names = [x.get_name() for x in self.profile.get_liked_recipes()]

        v_liked_recipes = [v_recipes[x] for x in range(len(self.recipes)) if self.recipes[x].get_name() in liked_recipes_names]
        print("Before score", v_liked_recipes)

        x  = v_liked_recipes[0]
        x = weight_recipe_with_score(x, 1)
        weighted_v_liked_recipes = []
        for i, recipe in enumerate(v_liked_recipes):
            recipe = weight_recipe_with_score(recipe, int(liked_recipes[i].get_score()))
            weighted_v_liked_recipes.append(recipe)



        # Modélisation du profil utilisateur
        kmeans = KMeans(n_clusters=5).fit(v_liked_recipes)
        centers =[x for x in kmeans.cluster_centers_]



