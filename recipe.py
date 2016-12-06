#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recipe :

	def _init_ (self,url,r_name,typ,diff,cost,gnumb,ptime,ctime,ingrs,instr) :
		self.url = url
		self.recipe_name = r_name
		self.type = typ
		self.difficulty = diff
		self.cost = cost
		self.guests_number = gnumb
		self.preparation_time = ptime
		self.cook_time = ctime
		self.ingredients = ingrs
		self.instruction = instr

	def get_url (self) :
		return self.url

	def get_recipe_name (self) :
		return self.recipe_name

	def get_type (self) :
		return self.type

	def get_difficulty (self) :
		return self.difficulty

	def get_cost (self) :
		return self.cost

	def get_guests_number (self) :
		return self.guests_number

	def get_preparation_time (self) :
		return self.preparation_time

	def get_cost_time 
		return self.cook_time

	def get_ingredients (self) :
		return self.ingredients

	def get_instruction (self) :
		return self.instruction

	