#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from tours import *

class Joueur:
	def __init__(self, carte, argent = 500, score = 0):
		self._argent = argent
		self._score = score
		self._carte = carte
		self._liste_tours = []
	@property
	def carte(self):
		return self._carte
	@property
	def liste_tours(self):
		return self._liste_tours
	@property
	def argent(self):
		return self._argent
	@property
	def score(self):
		return self._score

	def gestion_tour(self, event):
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			pos_x, pos_y = self.carte.objet_dans_case(event.pos)
			if self.carte.cases[pos_x][pos_y].type_objet == 5:
				# PROPOSER AMELIORATION OU REPARATION
				print ("Amélioration ? Réparation ?")
			elif self.carte.cases[pos_x][pos_y].type_objet == 102:
				pos_pix = pos_x*self.carte._largeur/self.carte._nb_cases_l\
				, pos_y*self.carte._hauteur/self.carte._nb_cases_h
				T = Tour(pos_pix, self)
				if T._cout_construction <= self._argent:
					self._liste_tours.append(T)
					self._argent -= T._cout_construction
					self.carte._cases[pos_x][pos_y]._type_objet = 5
				else:
					print ("Vous n'avez pas suffisamment d'argent.")

	def gain(self, difficulte):
		self._argent += self._score//difficulte
