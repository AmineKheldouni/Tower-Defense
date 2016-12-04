#!/usr/bin/python
#encoding: utf8

import pygame
from pygame.locals import *

from excel import *

import functools
from functools import partial
import copy
import sys
import numpy as np
import math as m
import copy
import numpy.random as rd
import time

class Carte:
	def __init__(self, hauteur=700, largeur=1250, nb_cases_h = 14, \
	nb_cases_l = 25,id_carte="carte_1"):
		self._id_carte=id_carte
		self._nb_cases_h = extract_carte(id_carte,0,1)
		self._nb_cases_l = extract_carte(id_carte,1,0)
		self._hauteur = self._nb_cases_h*50
		self._largeur = self._nb_cases_l*50
		self._grille = [[extract_carte(id_carte,i+1,j+1) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		self._objets = [[extract_carte(id_carte+"_objets",i+1,j+1) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)] # 5 = Case libre (verdure)
	@property
	def carte_couts(self):
		return self._carte_couts
	@property
	def largeur(self):
		return self._largeur
	@property
	def id_carte(self):
		return self._id_carte
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
		pas_l = int(self.largeur/self.nb_cases_l)
		pas_h = int(self.hauteur/self.nb_cases_h)
		return (objet_position[0]//pas_l, objet_position[1]//pas_h)

	def positionner_objet(self, pos_case):
		a = int(pos_case[0]*self.largeur/self.nb_cases_l)
		b = int(pos_case[1]*self.hauteur/self.nb_cases_h)
		return (a, b)

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
	def __init__(self, position, joueur, cout_entretien=100,\
	 cout_amelioration=20, hp = 100):
	 	self.vie_depart = hp
		self._vie = hp
		self._joueur = joueur
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._position = position
		self._joueur._carte[position] = "base"

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
