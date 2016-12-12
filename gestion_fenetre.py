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
	def __init__(self, position, type_objet="",tapis=0, id_graphic=0, is_chemin=0):
		self._position = position
		self._type_objet = type_objet # String de legend2
		self._tapis = tapis	# Int de legend1
		self._id_graphic = id_graphic
		self._est_chemin = is_chemin
	@property
	def position(self):
		return self._position
	@property
	def type_objet(self):
		return self._type_objet
	@property
	def tapis(self):
		return self._tapis
	@property
	def __setitem__(self, objet_id):
		self._type_objet = objet_id
	def set_id(self,new_id):
		self._id_graphic = new_id
	def est_attackable(self):
		return False
	@property
	def __getitem__(self):
		return self.type_objet
	def actualisation(self):
		None
	#Dis si l'armée peut marcher dessus
	def est_chemin(self):
		return self._est_chemin

class Emplacement(Case):
	def __init__(self, position, tapis, id_excel):
		super(Emplacement,self).__init__(position, "place_construction", tapis,id_excel)
# Pour faire un No_Objet : (self,position,graphic,arg,id_exel)
class Element_decor(Case):
	"""docstring for Element_decor."""
	def __init__(self, position, tapis, id_excel):
		super(Element_decor,self).__init__(position,"element_decor",tapis,id_excel)

class Base(Case):
	def __init__(self, position, tapis=0,id_excel=103):
	 	super(Base,self).__init__(position,"base",tapis,id_excel,0)
	 	self.vie_depart = 100
		self._vie = self.vie_depart
		self._cout_entretien = 100
		self._cout_amelioration = 20
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
	def is_attackable(self):
		return self._vie>0
	def dommage(self,degat):
		self._vie -= degat
		self._vie = max(0,self._vie)
		print(self._vie)
	def actualisation(self):
			if self._vie > self.vie_depart/2:
				self.set_id(103)
			elif self._vie >self.vie_depart/5 and self._vie <=self.vie_depart/2:
				self.set_id(104)
			else:
				self.set_id(105)

	def ameliorer(self):
		if self._joueur.argent >= self._cout_entretien:
			self._vie += 1
			self._joueur.argent -= self._cout_entretien
# = liste_entretien_base[id_entretien+1] => Creer une liste de couts
#d'entretiens sur un Excel, pour augmenter le cout
			self._cout_entretien += 1

class Carte:
	def __init__(self, hauteur=700, largeur=1250, nb_cases_h = 25, \
	nb_cases_l = 25,id_carte="carte_1"):
		self._liste_tours =[]
		self._liste_souces=[]
		self._pos_bases =[]

		self._id_carte=id_carte
		self._nb_cases_h = extract_carte(id_carte,0,1)
		self._nb_cases_l = extract_carte(id_carte,1,0)
		self._hauteur = hauteur
		self._largeur = largeur
		self.liste_sources = []
		self._cases =  [[ Case( (i,j), extract_carte(id_carte+"_objets",i+1,j+1),(extract_carte(id_carte,i+1,j+1))) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		# self._grille = [[ extract_carte(id_carte,i+1,j+1) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		dico_nom_id=cree_dico('legend2',1,0)
		dico_name_to_id_graph=cree_dico('legend2',1,2)
		for j in range(0,self.nb_cases_l):
			for i in range(0,self._nb_cases_h):
				ob = extract_carte(id_carte+"_objets",i+1,j+1)
				if(dico_nom_id[ob]=="source"):
					self._cases[j][i] = Element_decor((i,j),extract_carte(id_carte,i+1,j+1),ob)
					self.liste_sources.append((j, i))
				elif dico_nom_id[ob]=="base":
					self._cases[j][i] = Base((i,j),extract_carte(id_carte,i+1,j+1),ob)
					self._pos_bases.append((j,i))
				elif dico_nom_id[ob]=="place_construction":
					self._cases[j][i]= Emplacement((i,j),extract_carte(id_carte,i+1,j+1),ob)
				if(extract_carte(id_carte,i+1,j+1)==1):
					self._cases[j][i]._est_chemin=1;
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
	@property
	def cases(self):
		return self._cases

	def __contains__(self, position):
	    lig, col = position
	    return (lig >= 0) and (lig < self._nb_cases_l) and (col >= 0) \
		and (col < self._nb_cases_h)

	def __getitem__(self, position):
		lig, col = position
		if position in self:
			return self._cases[lig][col]

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

	def genere_decor(self,tab_objet):
		for j in range(len(tab_objet)):
			for i in range(tab_objet[j]):
				tmp1, tmp2 = np.random.randint(self.nb_cases_l-1), np.random.randint(1, self.nb_cases_h-1)
				while self._cases[tmp1][tmp2].tapis!=0:
					tmp1, tmp2 = np.random.randint(self.nb_cases_l-1), np.random.randint(self.nb_cases_h-1)
				pos_x, pos_y = self.positionner_objet((tmp1,tmp2))
				self._cases[tmp1][tmp2] = Element_decor((tmp1,tmp2),extract_carte(self._id_carte+"_objets",i+1,j+1),1000+j+1)
	def case_objet(self,i,j):
		return self._objets[i][j]

	def get_type_case(self, pos):
		return self[pos]._type_objet

	def est_case_chemin(self,pos):
		if      (pos[0]>=self.nb_cases_l) or (pos[1]>=self.nb_cases_h) or (pos[0]<0)or (pos[1]<0):
			return False
		else:
			return self._cases[pos[0]][pos[1]].est_chemin()

	def actualise(self):
		for i in range(self._nb_cases_l):
			for j in range(self._nb_cases_h):
				self._cases[i][j].actualisation();
