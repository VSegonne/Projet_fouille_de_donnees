from tkinter import *
from tkinter.messagebox import *
import random
import sys

class MakeMenuPan(Frame):

    def __init__(self, root, model):
        Frame.__init__(self, root)
        self.root = root
        root.geometry= "+450+200"
        self.model = model


        self.randomMenFrame = RandomMenuFrame(self, model)
        self.randomMenFrame.grid(row=0, column=0, rowspan=2)

        self.recommendFrame = RecommendFrame(self, model)
        self.recommendFrame.grid(row=0, column=1, padx=5)

        self.userMenuFrame = UserMenuFrame(self, model)
        self.userMenuFrame.grid(row=1, column=1, sticky="N")

        self.grid_columnconfigure(1, minsize=400)
        self.grid_rowconfigure(1, minsize=360)

        self.pack_propagate(False)



class RecommendFrame(Frame):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Frame.__init__(self, frame, borderwidth=2, relief="ridge")

        Label(self,text="Vous aimerez peut être !").grid(row=0)

        for i, recipe in enumerate(self.model.recommended_recipes):
            if i < 3:
                recommendRecipe = RecommendRecipeFrame(self, self.model, recipe)
                recommendRecipe.grid(row=i+1, pady=5, padx=5)


class RecommendRecipeFrame(Frame):
    def __init__(self, frame, model, recipe):
        self.frame = frame
        self.model = model
        self.recipe =recipe
        Frame.__init__(self, frame, relief="raised", width=350, height=90, borderwidth=2)

        recipe_name = Label(self, text= recipe.get_name())
        recipe_name.grid(row=0, column=0, sticky="W", padx=10, pady=5)

        likeButton = LikeButton(self, model)
        likeButton.grid(row=0, column=1)

        dislikeButton = DislikeButton(self, model)
        dislikeButton.grid(row=1, column=1)

        # info + Ajouter

        infoButton = InfoRecipeButton(self, model)
        infoButton.grid(row=1, column=0, sticky="W")

        addRecipeButton = AddRecipeButton(self, model)
        addRecipeButton.grid(row=0, column=2)

        switchButton = SwitchButton(self, model)
        switchButton.grid(row=1, column=2)

        self.grid_columnconfigure(0, minsize=400)

class LikeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="J'aime", command=self.like)

    def like(self):
        self.background="green"
        self.frame.configure(bg="green")
        self.model.add_liked_recipe_to_profile(self.model.profile.get_name(), self.frame.recipe)

class DislikeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Je n'aime pas", command=self.dislike)

    def dislike(self):
        self.frame.configure(background="red")
        self.model.add_disliked_recipe_to_profile(self.model.profile.get_name(), self.frame.recipe)
        print("Je n'aime pas")


class UserMenuFrame(Frame):
    def __init__(self, frame, model ):
        self.model = model
        self.frame =frame
        Frame.__init__(self, frame, width=300,height=90, borderwidth=2, relief="raised")

        Label(self, text="Votre Menu").grid(row=0)



        self.grid_columnconfigure(0, minsize=510)
        self.pack_propagate(False)

        finishButton = FinishButton(self, model)
        finishButton.grid(row=8)

    def update(self):
        for i, recipe in enumerate(self.model.menu):
            recipe = RecipeInMenuFrame(self, self.model, recipe)
            recipe.grid(row=i+1)

class RecipeInMenuFrame(Frame):
    def __init__(self, frame, model, recipe):
        self.frame = frame
        self.model = model
        self.recipe = recipe
        Frame.__init__(self, frame)

        Label(self, text=self.recipe.get_name()).grid(row=0, column=0)

        SuppRecipeButton(self, self.model).grid(row=0, column=1)



        self.pack_propagate(False)


class RandomMenuFrame(Frame):
    def __init__(self, frame, model):
        Frame.__init__(self, frame, relief= "ridge", borderwidth=2)
        self.frame = frame
        self.model = model

        Label(self, text="Le Menu que je vous propose!").grid(row=0)
        self.random_recipes = random.sample(self.model.profile.get_liked_recipes(), len(self.model.profile.get_liked_recipes()))
        print(len(self.random_recipes))
        for i in range(7):
            recipe = RandomRecipeFrame(self, model, self.random_recipes[i])
            recipe.grid(row=i+1, padx=10, pady=5)

class RandomRecipeFrame(Frame):
    def __init__(self, frame, model, recipe):
        Frame.__init__(self, frame, relief="raised", width=350, height=90, borderwidth=2)
        self.frame = frame
        self.model = model
        self.recipe = recipe

        Label(self, text= recipe.get_name()).grid(row=0, column=0, sticky="W", padx=10, pady=5)

        self.grid_columnconfigure(0, minsize=400)

        addButton = AddRecipeButton(self, model)
        addButton.grid(row=0, column=1)

        dislikeButton = DislikeButton(self, model)
        dislikeButton.configure(text="Je n'aime plus")
        dislikeButton.grid(row=1, column=1)

        infoButton = InfoRecipeButton(self, model)
        infoButton.grid(row=1, sticky="W")

        switchButton = SwitchButton(self, model)
        switchButton.grid(row=3, column=1)


class AddRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Ajouter",command=self.add)

    def add(self):
        self.model.add_recipe_to_menu(self.frame.recipe)
        self.frame.frame.frame.userMenuFrame.update()



class SuppRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame =frame
        self.model =model
        Button.__init__(self, frame, text="Supprimer", command=self.sup)

    def sup(self):
        self.model.sup_recipe_from_menu(self.frame.recipe)
        self.frame.destroy()
        print(self.model.menu)

class InfoRecipeButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Details", command=self.get_info)

    def get_info(self):
        recipe = self.frame.recipe
        text = "Type : " + recipe.get_type() + "\n\n"\
            + "Difficulté : " + recipe.get_difficulty() + "\n\n"\
            + "Coût : " + recipe.get_cost() + "\n\n" \
            + "Nb de couverts : " + recipe.get_guests_number() + "\n\n"\
            + "Temps de préparation : " + recipe.get_preparation_time() + "\n\n"\
            + "Temps de cuisson : " + recipe.get_cook_time() + "\n\n" \
            + "Ingredients : " + recipe.get_ingredients().replace('|',' ') + "\n\n"


        showinfo(self.frame.recipe.get_name(), text)


class SwitchButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Switch", command=self.switch)

    def switch(self):

        if isinstance(self.frame, RandomRecipeFrame):
            grid_info = self.frame.grid_info()
            i = random.randint(1, len(self.model.profile.get_liked_recipes()))-1
            randomRecipe = RandomRecipeFrame(self.frame.frame, self.model, self.model.profile.get_liked_recipes()[i])
            randomRecipe.grid(row=grid_info['row'], column=grid_info["column"])
            self.frame.destroy()
        else:
            grid_info = self.frame.grid_info()
            i = random.randint(1, len(self.model.recommended_recipes))-1
            recommendRecipe = RecommendRecipeFrame(self.frame.frame, self.model, self.model.recommended_recipes[i])
            recommendRecipe.grid(row=grid_info['row'], column=grid_info["column"])
            self.frame.destroy()


class FinishRecipeFrame(Frame):
    def __init__(self, frame, model, recipe):
        self.frame = frame
        self.model = model
        self.recipe = recipe
        Frame.__init__(self, frame, width=400, height=700, borderwidth=2, relief="raised")

        name = Label(self, text= recipe.get_name())
        name.grid(row=0, column=0)

        infoButton = InfoRecipeButton(self, self.model)
        infoButton.grid(row=0, column=1)

        self.grid_columnconfigure(0, minsize=400)

        self.pack_propagate(False)

class FinishButton(Button):
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        Button.__init__(self, frame, text="Terminer!", command=self.validate)

    def validate(self):
        if len(self.model.menu) < 7:
            showinfo('Attention!', "Nombre de repas insuffisant")
        else:
            for i, recipe in enumerate(self.model.menu):
                self.model.increment_score_by_one(self.model.profile.get_name(), recipe)
                root = self.frame.frame.root
                self.frame.frame.destroy()
                root.geometry="+300+400"
                f = FinishRecipeFrame(root, self.model, recipe)
                f.grid(row= i+1, pady=15, padx=15)
                f.grid_rowconfigure(i+1, minsize=10)




