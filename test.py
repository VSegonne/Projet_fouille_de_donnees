from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from scipy.spatial import distance
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from DataBaseManager import *
import operator
import sys


create_recipes_database_from_textFile("NewDB","recipes_index_A.txt")
