#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from tours import *

class Joueur:
	def __init__(self, carte, argent = 1000, score = 0):
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

	def score(self,point):
		self._score+=point
	def argent(self,tune):
		self._argent+=tune

	def actualise_valeurs(self, (argent,point)):
		self.argent(argent)
		self.score(point)

	def gestion_tour(self, event):
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			pos_x, pos_y = self.carte.objet_dans_case(event.pos)
			if (pos_x, pos_y) in self.carte and self.carte.get_type_case((pos_x,pos_y)) == "tour":
				# PROPOSER AMELIORATION OU REPARATION
				print ("Amélioration ? Réparation ?")
			elif (pos_x, pos_y) in self.carte and self.carte.get_type_case((pos_x,pos_y)) == "place_construction":
				pos_pix = pos_x*self.carte._largeur/self.carte._nb_cases_l\
				, pos_y*self.carte._hauteur/self.carte._nb_cases_h
				T = Tour(pos_pix)
				if T._cout_construction <= self._argent:
					self._liste_tours.append(T)
					self._argent -= T._cout_construction
					self.carte._cases[pos_x][pos_y] = T
				else:
					print ("Vous n'avez pas suffisamment d'argent.")
	def ameliorer_tour(self, T, Vue):
		if self._argent >= T.cout_amelioration:
			Vue.animation_amelioration(T)
			self._argent -= T.cout_amelioration
			T.ameliore(self.carte)

	def reparer_tour(self, T):
		if self._argent >= T.cout_entretien and T.munitions < \
		T.munitions_max:
			self._argent -= T.cout_entretien
			T.repare()

	def construire_tour(self, id_tour, pos):
		if(id_tour == 0):
			T = Tour(self.carte.positionner_objet(pos), id_tour)
		elif(id_tour == 2):
			T = Tour_Glace(self.carte.positionner_objet(pos), id_tour)
		elif(id_tour == 1):
			T = Tour_Feu(self.carte.positionner_objet(pos), id_tour)
		assert(self.carte.get_type_case(pos) == "place_construction")
		if T._cout_construction <= self._argent:
			self._liste_tours.append(T)
			self._argent -= T._cout_construction
			self._carte._cases[pos[0]][pos[1]] = T
			self._carte._cases[pos[0]][pos[1]]._type_objet = "tour"
			return True
		else:
			return False
