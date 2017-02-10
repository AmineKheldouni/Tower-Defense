#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from tours import *

class Joueur:
	def __init__(self, argent = 500, score = 0):
		self._argent = argent
		self._score = score
		self._liste_tours = []

	@property
	def liste_tours(self):
		return self._liste_tours
	@property
	def argent(self):
		return self._argent
	@property
	def score(self):
		return self._score

	def gain_score(self,point):
		self._score+=point
	def gain_argent(self,gain):
		self._argent+= gain

	def actualise_valeurs(self, pos):
		""" pos = [argent, point_score] """
		self.gain_argent(pos[0])
		self.gain_score(pos[1])

	def ameliorer_tour(self, T, C, Vue=None):
		if self._argent >= T.cout_amelioration:
			if Vue!=None:
				Vue.animation_amelioration(T, C)
			self._argent -= T.cout_amelioration
			T.ameliore(C)
			return True

	def reparer_tour(self, T):
		if self._argent >= T.cout_entretien and T.munitions < \
		T.munitions_max:
			self._argent -= T.cout_entretien
			T.repare()
			return True
		return False

	def construire_tour(self, id_tour, pos, C):
		if(id_tour == 0):
			T = Tour(C.positionner_objet(pos), id_tour)
		elif(id_tour == 2):
			T = Tour_Glace(C.positionner_objet(pos), id_tour)
		elif(id_tour == 1):
			T = Tour_Feu(C.positionner_objet(pos), id_tour)

		if T._cout_construction <= self._argent:
			self._liste_tours.append(T)
			self._argent -= T._cout_construction
			C[pos] = T
			C[pos]._type_objet = "tour"
			return True
		else:
			return False
