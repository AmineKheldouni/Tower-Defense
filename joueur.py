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
	def gestion_tour(self, event):
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			pos_x, pos_y = self._carte.objet_dans_case(event.pos)
			if self._carte[pos_x, pos_y] == "tour":
				# PROPOSER AMELIORATION OU REPARATION
				print "Amélioration ? Réparation ?"
			elif self._carte[pos_x, pos_y] == "place construction":
				pos_pix = pos_x*self._carte._largeur/self._carte._nb_cases_l\
				, pos_y*self._carte._hauteur/self._carte._nb_cases_h
				T = Tour(pos_pix, self)
				if T._cout_construction <= self._argent:
					self._liste_tours.append(T)
					self._argent -= T._cout_construction
					self._carte[pos_x, pos_y] = "tour"
					if pos_y>0:
						self._carte[pos_x, pos_y-1] = "tour"
				else:
					print "Vous n'avez pas suffisamment d'argent."
	def affichage_portee(self, fenetre):
		pos = pygame.mouse.get_pos()
		pos_case = self.carte.objet_dans_case(pos)
		if self._carte[pos_case] == "tour" :
			tmp = self._carte.objet_dans_case(pos)
			pos = self._carte.positionner_objet(tmp)
			for T in self._liste_tours:
				if T._position == pos:
					pos = self._carte.positionner_objet((tmp[0]+0.5, tmp[1]+0.5))
					pygame.draw.circle(fenetre, (255, 255, 255), (int(pos[0]), int(pos[1])), 100, 2) # 100 = PORTEE TOUR
