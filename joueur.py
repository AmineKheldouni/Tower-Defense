#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from tours import *

class Joueur:
	def __init__(self, carte, argent = 10, score = 0):
		self._argent = argent
		self._score = score
		self._liste_tours = []
		self._carte = carte
	def construit_tour(self, event):
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				pos_x, pos_y = self._carte.objet_dans_case(event.pos)
				if self._carte[pos_x, pos_y] == 2:
					pos_pix = pos_x*self._carte._largeur/self._carte._nb_cases_l\
					, pos_y*self._carte._hauteur/self._carte._nb_cases_h
					T = Tour(pos_pix, 1)
					if T._cout_construction <= self._argent:
						self._liste_tours.append(T)
						self._argent -= T._cout_construction
						self._carte[pos_x, pos_y] = 10
					else:
						print "Vous n'avez pas suffisamment d'argent."
