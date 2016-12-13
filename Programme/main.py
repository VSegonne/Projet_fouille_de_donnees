from Application import *
from DataBaseManager import  *
from utils import *
import sys
from DataBaseManager import *
from utils import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import operator
import random
from ProfileManager import *
from Profile import *

# Creat DB

#DBM = DataBaseManager("Recipes.db", "Profile.db")
#recipes = DBM.load_recipes_from_database2("Recipes.db")
#DBM.create_profile_table('Vincent')
#r1 = Recipe("ww.test.org", "soupe aux poireaux", "plat principal", "Facile", "pas cher", "2", "40", "40", "poireaux|pommesdeterre|oignon", "faire cuire la soupe", "like", "2")
#r2 = Recipe("ww.test.org", "soupe aux champignons", "plat principal", "Moyennement difficile", "difficile", "2", "40", "40", "champignon|salade|carottes", "faire cuire la soupe", "dislike", "0")
#liked_recipes = [r1]
#DBM.add_liked_recipes_to_profile('Vincent', liked_recipes)
#vince_profile = DBM.load_profile_from_database('Vincent')
#print(vince_profile.get_name())





#==============================================
app = Application("Recipes.db", "Profile.db")
app.start()
