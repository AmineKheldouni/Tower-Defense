#!/usr/bin/python
#encoding: utf8

import pygame
from pygame.locals import *

from csvuser import *
from case import *

import functools
from functools import partial
import copy
import sys
import numpy as np
import copy
import numpy.random as rd


class Carte:
	def __init__(self,id_carte="cartes_carte1", hauteur=700, largeur=1250, nb_cases_h = 25, \
	nb_cases_l = 25):
		self._liste_tours =[]
		self._liste_souces=[]
		self._pos_bases =[]
		self._id_carte=id_carte
		self._nb_cases_h = ExtractIntFromFile(id_carte+".csv",0,1)
		self._nb_cases_l = ExtractIntFromFile(id_carte+".csv",0,2)
		self._hauteur = hauteur
		self._largeur = largeur
		self._pos_sources = []
		self._cout_chemin=[[ 1000 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		self._cout_case  =[[ 1 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		tab_carte=LoadIntFromFile(id_carte+".csv",1,self._nb_cases_l,1,self._nb_cases_h)
		tab_carte_objets=LoadIntFromFile(id_carte+"objets.csv",1,self._nb_cases_l,1,self._nb_cases_h)
		self._cases =  [[ Case( (i,j), tab_carte_objets[i][j], tab_carte[i][j] ) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		# self._grille = [[ extract_carte(id_carte,i+1,j+1) for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
		dico_nom_id=DicoFromFile("cartes_legend2.csv",2,16,1,0)
		dico_name_to_id_graph=DicoFromFile("cartes_legend2.csv",2,16,1,2)
		for j in range(0,self.nb_cases_l):
			for i in range(0,self._nb_cases_h):
				ob = tab_carte_objets[i][j]
				if(dico_nom_id[ob]=="source"):
					self._cases[j][i] = Source((i,j),tab_carte[i][j],ob)
					self._pos_sources.append((j, i))
				elif dico_nom_id[ob]=="base":
					self._cases[j][i] = Base((i,j),tab_carte[i][j],ob)
					self._pos_bases.append((j,i))
				elif dico_nom_id[ob]=="place_construction":
					self._cases[j][i]= Emplacement((i,j),tab_carte[i][j],ob)
				chemin = tab_carte[i][j]
				if(chemin==1):
					self._cases[j][i]._est_chemin=chemin;
					self._cases[j][i]._tapis = 1;
					self.set_cout_case((i,j),1)

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
	# def __contains__(self, pos):
	# 	return (pos[0]<self.nb_cases_l) and (pos[1]<self.nb_cases_h) or (pos[0]>=0)or (pos[1]>=0)

	def __contains__(self, position):
	    lig, col = position
	    return (lig >= 0) and (lig < self._nb_cases_l) and (col >= 0) \
		and (col < self._nb_cases_h)

	def __getitem__(self, position):
		lig, col = position
		if position in self:
			return self.cases[lig][col]

	def __setitem__(self, position, valeur):
	    lig, col = position
	    if position in self:
	        self._cases[lig][col] = valeur

# Getteur setter des cout
	def get_cout_chemin(self,(i,j)):
		return self._cout_chemin[i][j]

	def get_cout_case(self,(i,j)):
		return self._cout_case[i][j]

	def set_cout_chemin(self,(i,j),cout):
		self._cout_chemin[i][j] = cout;

	def set_cout_case(self,(i,j),cout):
		self._cout_case[i][j] = cout;


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
		max_ligne_tab_objet=max([tab_objet[j] for j in range(len(tab_objet))])
		tab_carte_objets=LoadIntFromFile(self._id_carte+"objets.csv",1,max_ligne_tab_objet,1,len(tab_objet))
		for j in range(len(tab_objet)):
			for i in range(tab_objet[j]):
				tmp1, tmp2 = np.random.randint(self.nb_cases_l-1), np.random.randint(1, self.nb_cases_h-1)
				while self._cases[tmp1][tmp2]._tapis!=0 and self.get_type_case((tmp1,tmp2))!="place_construction":
					tmp1, tmp2 = np.random.randint(self.nb_cases_l-1), np.random.randint(self.nb_cases_h-1)
				pos_x, pos_y = self.positionner_objet((tmp1,tmp2))
				self._cases[tmp1][tmp2] = Element_decor((tmp1,tmp2),1000+j+1,0)


#@getter et setter
	def case_objet(self,i,j):
		return self._objets[i][j]

	def get_case(self,i,j):
		return self._cases[i][j]

	def get_case(self,pos):
		return self._cases[pos[0]][pos[1]]

	def get_type_case(self, pos):
		return self[pos]._type_objet

	def get_base(self,i):
		return self.get_case(self._pos_bases[i])

	def get_source(self,i):
		return self.get_case(self._pos_sources[i])

	def est_case_chemin(self,pos,soldat_direction=0):
		if  (pos[0]>=self.nb_cases_l) or (pos[1]>=self.nb_cases_h) or (pos[0]<0)or (pos[1]<0):
			return False
		else:
			return self._cases[pos[0]][pos[1]].est_chemin(soldat_direction)

	def actualise(self):
		for pos in self._pos_bases:
			if(self._cases[pos[0]][pos[1]].actualisation()):
				self.base_est_morte(pos)
		for i in range(self._nb_cases_l):
			for j in range(self._nb_cases_h):
				self._cases[i][j].actualisation()

#Gestion de la carte de cout
	def reinitialiser_cout_chemin(self):
		for i in range(self._nb_cases_h):
			for j in range(self._nb_cases_l):
				self._cout_chemin[j][i] = 1000

	def rec_actualise_cout_chemin(self, pos_case, vect_voisin, cout_actuel):
		self.set_cout_chemin(pos_case, cout_actuel)
		for i in range( len(vect_voisin)):
			#le soldat va dans l'autre sens et est tourné dans le sens opposé
			direction = i+2%4
			voisin = vect_voisin[i]
			tmp_a, tmp_b = (pos_case[0]+voisin[0]), (pos_case[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			# Si je suis un chemin et que Cout_CHemin +COut_case < Cout_chemin je remplace et j'actualise
			if (self.est_case_chemin(case_voisin,direction)) and \
			(self.get_cout_case(case_voisin) + self.get_cout_chemin(pos_case) < self.get_cout_chemin(case_voisin) ):
				new_cost = self.get_cout_case(case_voisin) + self.get_cout_chemin(pos_case)
				self.rec_actualise_cout_chemin(case_voisin, vect_voisin, new_cost )

	def actualise_cout_chemin(self):
		self.reinitialiser_cout_chemin()
		voisin = [(0, 1), (-1,0), (0, -1), (1, 0)]
		for i,pos_base in enumerate(self._pos_bases):
			if(not self.get_base(i)._est_mort):
				self.rec_actualise_cout_chemin(pos_base, voisin, 1 )

#Gestion des sources et des bases

	def base_est_morte(self, pos):
		'''s'active quand un base meurt modifie la carte afin que les ennemis n'y accèdent plus'''
		dico_dir_vers_entier = { (0,1) : -3 , (0,-1) : -1 , (1,0) : -4 , (-1,0) : -2}
		old_pos = pos
		pos_act = pos
		voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]
		liste_voisins =[]
		for voisin in voisins:
			tmp_a, tmp_b = int(pos_act[0]+voisin[0]), int(pos_act[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			if self.est_case_chemin(case_voisin) and case_voisin != old_pos:
				liste_voisins.append(case_voisin)
		if(len(liste_voisins)==1):
			while len(liste_voisins)<=1:
				liste_voisins =[]
				for voisin in voisins:
					tmp_a, tmp_b = int(pos_act[0]+voisin[0]), int(pos_act[1]+voisin[1])
					case_voisin = (tmp_a, tmp_b)
					if self.est_case_chemin(case_voisin) and case_voisin != old_pos:
						liste_voisins.append(case_voisin)
				if(len(liste_voisins)==0):
					print("la carte est une ligne droite non ?")
					return 0
				if(len(liste_voisins)==1):
					old_pos = pos_act
					pos_act=liste_voisins[0]
			#On est sur une intersection il faut donc modifier old_pos pour empêcher les ennemis de l'intersection d'y accéder
			direction = (old_pos[0]-pos_act[0],old_pos[1]-pos_act[1])
			self._cases[old_pos[0]][old_pos[1]]._est_chemin= dico_dir_vers_entier[direction]
		else :
			# La base ou la source a plusieurs voisins et il ne faut pas toucher au reste.
			None

	def initialiser_source(self, i):
		pos_case = self._pos_sources[i]
		source = self.get_source(i)
		voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]
		for i,voisin in enumerate(voisins):
			tmp_a, tmp_b = (pos_case[0]+voisin[0]), (pos_case[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			assert(case_voisin != (source._position))
			if (self.est_case_chemin(case_voisin,(i+2)%4)):
				source._direction.append(i)

	def initialiser_sources(self):
		for i in range(len(self._pos_sources)):
			self.initialiser_source(i)
			self.base_est_morte(self._pos_sources[i])

	def initialiser_carte(self, vec_decor=[]):
		self.genere_decor(vec_decor)
		self.actualise_cout_chemin()
		self.initialiser_sources()
