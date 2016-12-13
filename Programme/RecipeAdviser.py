from utils import  *
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator


class RecipeAdviser():
    def __init__(self, profile, recipes):
        self.profile = profile
        self.recipes= recipes


    def generate_recommended_recipes(self):
        v_recipes = vectorize_recipes2(self.recipes)
        liked_recipes = [x for x in self.profile.get_liked_recipes()]
        liked_recipes_names = [x.get_name() for x in self.profile.get_liked_recipes()]

        v_liked_recipes = [v_recipes[x] for x in range(len(self.recipes)) if self.recipes[x].get_name() in liked_recipes_names]

        weighted_v_liked_recipes = []

        # Pondération des recettes préférées
        l = float(len(v_liked_recipes))

        for i, recipe in enumerate(v_liked_recipes):
            score = int(liked_recipes[i].get_score()) / l
            recipe = weight_recipe_with_score(recipe, score)
            weighted_v_liked_recipes.append(recipe)


        best_k = get_best_k(weighted_v_liked_recipes)


        # Modélisation du profil utilisateur
        kmeans = KMeans(n_clusters=best_k).fit(weighted_v_liked_recipes)
        centers =[x for x in kmeans.cluster_centers_]


        unranked_cos_sim = []

        # On trie les similarités pour avoir les meilleurs au début de la liste

        # Phase de recommandation
        for i, recipe in enumerate(self.recipes):
            if recipe.get_name() not in liked_recipes_names:
                matrix = centers + v_recipes[i]
                cos_matrix = cosine_similarity(matrix)
                score_best_sim = max(cos_matrix[0][1:])
                unranked_cos_sim.append((i,score_best_sim))


        sorted_recommendation = sorted(unranked_cos_sim,key=operator.itemgetter(1), reverse=True)[:10]


        recommended_recipes = []
        for recipe_tuple in sorted_recommendation:
            recommended_recipes.append(self.recipes[recipe_tuple[0]])

        return recommended_recipes


