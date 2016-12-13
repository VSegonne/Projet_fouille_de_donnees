
class Profile():

    def __init__(self, profile_name):
        self.name = profile_name
        self.liked_recipes = None
        self.disliked_recipes = None

    def get_name(self):
        return self.name
    def get_liked_recipes(self):
        return self.liked_recipes

    def get_disliked_recipes(self):
        return self.disliked_recipes

    def set_liked_recipes(self, liked_recipes):
        self.liked_recipes

    def set_disliked_recipes(self, disliked_recipes):
        self.disliked_recipes



