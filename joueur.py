#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from tours import *

class Joueur:
	def __init__(self, argent = 100000, score = 0):
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
		self._score +=point

	def gain_argent(self, gain):
		self._argent += gain

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

	def miseajour_carte_cout_tours(self, carte):
		carte.reinitialiser_cout_case()
		for tour in self._liste_tours:
			if(tour._munitions>0):
				portee=tour._portee
				(pos_x,pos_y)=carte.objet_dans_case(tour._position)
				for i in range(-portee,portee+1,1):
					for j in range(-portee,portee+1,1):
						pos = (pos_x+i, pos_y+j)
						if pos in carte:
							carte.set_cout_case(pos,carte.get_cout_case(pos)+tour._degat*tour._vitesse)
		carte.actualise_cout_chemin()
