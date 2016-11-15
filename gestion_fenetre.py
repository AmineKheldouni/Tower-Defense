#!/usr/bin/python
#encoding: utf8

import pygame
from pygame.locals import *

import functools
from functools import partial
import copy
import sys
import numpy as np
import math as m


class Carte:
	def __init__(self, hauteur=800, largeur=1000, nb_cases_h = 16, \
	nb_cases_l = 20):
		self._hauteur = hauteur
		self._largeur = largeur
		self._nb_cases_h = nb_cases_h
		self._nb_cases_l = nb_cases_l
		self._grille = [["herbe" for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)] # 5 = Case libre (verdure)
		self._carte_couts = [10000]
		self._liste_construction = []
		self._liste_chemin = []
		self._liste_bases = [((nb_cases_l-1)*largeur/nb_cases_l, hauteur/nb_cases_h*(nb_cases_h//2))]
		self._liste_decor = []

	@property
	def carte_couts(self):
		return self._carte_couts
	@property
	def largeur(self):
		return self._largeur
	@property
	def hauteur(self):
		return self._hauteur
	@property
	def nb_cases_h(self):
		return self._nb_cases_h
	@property
	def nb_cases_l(self):
		return self._nb_cases_l
	def __contains__(self, position):
	    lig, col = position
	    return (lig >= 0) and (lig < self._nb_cases_l) and (col >= 0) \
		and (col < self._nb_cases_h)

	def __getitem__(self, position):
		lig, col = position
		if position in self:
			return self._grille[lig][col]

	def __setitem__(self, position, valeur):
	    lig, col = position
	    if position in self:
	        self._grille[lig][col] = valeur

	def objet_dans_case(self, objet_position):
		""" Retourne les coordonnées de la case de l'objet """
		for i in range(0, self._nb_cases_l):
			for j in range(0, self._nb_cases_h):
				if objet_position[0]-i*self.largeur/self.nb_cases_l >=0 and \
				objet_position[0]-i*self.largeur/self.nb_cases_l < self.largeur/self.nb_cases_l \
				and objet_position[1]-j*self.hauteur/self.nb_cases_h >=0 and \
				objet_position[1]-j*self.hauteur/self.nb_cases_h < self.hauteur/self.nb_cases_h:
					return i, j
	def positionner_objet(self, pos_case):
		return (pos_case[0]*self.largeur/self.nb_cases_l, pos_case[1]*self.hauteur/self.nb_cases_h)

	def centre_case(self, (i, j)):
		return (int((i+0.5)*self.largeur/self.nb_cases_l), int((j+0.5)*self.hauteur/self.nb_cases_h))
	def case_construction(self, i, j):
		self._liste_construction.append((i, j))
		self._grille[i, j] = "place construction"

	def case_chemin(self, i, j):
		self._liste_chemin.append((i, j))
		self._grille[i, j] = "chemin" # La case est un chemin

	def case_tour(self, i, j):
		self._grille[i, j] = "tour" # La case est une tour

	def case_decor(self, i, j):
		self._liste_decor.append((i, j))
		self._grille[i, j] = "decor" # La case est un rocher/arbre
	def case_base(self, i, j):
		self._liste_bases.append((i, j))
		self._grille[i, j] = "base" # La case est un rocher/arbre

	def case_utilisateur(self, i, j):
		self._grille[i, j] = "utilisateur" # La case est un rocher/arbre

class Base:
	def __init__(self, position, carte, cout_entretien=100,\
	 cout_amelioration=20, hp = 1):
		self._vie = hp
		self._carte = carte
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._position = position
		self._carte[position] = "base" # 6 = base

	@property
	def vie(self):
		return self._vie
	@property
	def position(self):
		return self._position

	def est_morte(self):
		if self.vie == 0:
			return True
		return False

	def ameliorer(self):
		if self._joueur.argent >= self._cout_entretien:
			self._vie += 1
			self._joueur.argent -= self._cout_entretien
# = liste_entretien_base[id_entretien+1] => Creer une liste de couts
#d'entretiens sur un Excel, pour augmenter le cout
			self._cout_entretien += 1
