#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recipe :

    def __init__ (self, url , name, typ, difficulty, cost, guests_number, preparation_time, cook_time, ingredients, instructions, opinion=None, score=None):
        self.url = url
        self.name = name
        self.typ = typ
        self.difficulty = difficulty
        self.cost = cost
        self.guests_number = guests_number
        self.preparation_time = preparation_time
        self.cook_time = cook_time
        self.ingredients = ingredients
        self.instructions = instructions
        self.opinion = opinion
        self.score = score

    def get_url (self):
        return self.url

    def get_name (self):
        return self.name

    def get_type (self):
        return self.typ

    def get_difficulty (self):
        return self.difficulty

    def get_cost (self):
        return self.cost

    def get_guests_number (self):
        return self.guests_number

    def get_preparation_time (self):
        return self.preparation_time

    def get_cook_time(self):
        return self.cook_time

    def get_ingredients (self):
        return self.ingredients

    def get_instructions (self):
        return self.instructions

    def get_opinion(self):
        return self.opinion

    def get_score(self):
        return self.score

    def set_opinion(self, opinion):
        self.opinion = opinion

    def set_score(self, score):
        self.score = score
