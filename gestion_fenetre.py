#!/usr/bin/python
#encoding: utf8

import pygame
from pygame.locals import *

from excel import *
from objets_interraction import *

import functools
from functools import partial
import copy
import sys
import numpy as np
import math as m
import copy
import numpy.random as rd
import time


class Case(object):
	def __init__(self, position, type_objet="", type_case=0, id_objet=0, constructible=0, dimensions=0):
		self._position = position
		self._type_objet = type_objet
		self._type_case = type_case
		self._id_objet=id_objet;
		self._constructible=constructible
		self.dimensions = dimensions # dimensions = [largeur/nb_largeur, longueur/nb_longueur]
	@property
	def position(self):
		return self._position
	@property
	def type_objet(self):
		return self._type_objet
	@property
	def type_case(self):
		return self._type_case
	@property
	def __setitem__(self, objet_id):
		self._type_objet = objet_id
	@property
	def __getitem__(self):
		return self.type_objet


# Pour faire un No_Objet : (self,position,graphic,arg,id_exel)
class Element_decor(Case):
	"""docstring for Element_decor."""
	def __init__(self,position,type_case,id_exel):
		super(Element_decor,self).__init__(position,"element_decor", type_case,id_exel)

# class Source(Case):
# 	def __init__(self, position,id_exel=101):
# 		super(Source,self).__init__(position,id_exel,0)

class Base(Case):
	def __init__(self, position, cout_entretien=100,\
	 cout_amelioration=20, hp = 100,id_exel=103):
	 	super(Base,self).__init__(position,id_exel,0)
	 	self.vie_depart = hp
		self._vie = hp
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
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

class Chemin(Case):
		def __init__(self,position,type_case,id_exel):
			super(Element_decor,self).__init__(position,"element_decor", 1,1)


class Carte:
	def __init__(self, hauteur=400, largeur=1250, nb_cases_h = 8, \
	nb_cases_l = 25,id_carte="carte_1"):
		self._id_carte=id_carte
		self._nb_cases_h = extract_carte(id_carte,0,1)
		self._nb_cases_l = extract_carte(id_carte,1,0)
		self._hauteur = self._nb_cases_h*50
		self._largeur = self._nb_cases_l*50
		self._cases =  [[ Case( (i,j), extract_carte(id_carte+"_objets",i+1,j+1),(extract_carte(id_carte,i+1,j+1))) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		self._grille = [[ extract_carte(id_carte,i+1,j+1) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		dico_nom_id=cree_dico('legend2',1,0)
		for j in range(0,self.nb_cases_l):
			for i in range(0,self._nb_cases_h):
				ob = extract_carte(id_carte+"_objets",i+1,j+1)
				if(dico_nom_id[ob]=="source"):
					self._cases[j][i] = Element_decor((i,j),extract_carte(id_carte,i+1,j+1),ob)
				elif dico_nom_id[ob]=="base":
					self._cases[j][i] = Element_decor((i,j),extract_carte(id_carte,i+1,j+1),ob)
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
	def genere_decor(self,tab_objet):
		for j in range(len(tab_objet)):
			for i in range(tab_objet[j]):
				tmp1, tmp2 = np.random.randint(self.nb_cases_l-1), np.random.randint(1, self.nb_cases_h-1)
				while self[tmp1, tmp2] !=0:
					tmp1, tmp2 = np.random.randint(self.nb_cases_l-1), np.random.randint(self.nb_cases_h-1)
				pos_x, pos_y = self.positionner_objet((tmp1,tmp2))
				self._cases[tmp1][tmp2] = Element_decor((tmp1,tmp2),extract_carte(self._id_carte+"_objets",i+1,j+1),1000+j+1)
	def case_objet(self,i,j):
		return self._objets[i][j]
