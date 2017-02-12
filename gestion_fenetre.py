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
from utils import *

class Carte:
	def __init__(self,id_carte, resolution_h, resolution_l):
		self._liste_tours_actuelle =[]
		self._liste_tours_a_actualise=[]
		self._liste_souces=[]
		self._pos_bases =[]
		self._id_carte=id_carte
		self._nb_cases_h = ExtractIntFromFile(id_carte+".csv",0,1)
		self._nb_cases_l = ExtractIntFromFile(id_carte+".csv",0,2)
		# Le menu prend les 20% du bas
		self._hauteur = int(resolution_h*0.8)
		self._largeur = resolution_l
		self._pos_sources = []
		self._cout_chemin=[[ 1000 for i in range(self._nb_cases_h)] for j in \
		range(self._nb_cases_l)]
		self._cout_case  =[[ 1 for i in range(self._nb_cases_h)] for j in \
		range(self._nb_cases_l)]
		tab_carte=LoadIntFromFile(id_carte+".csv",1,self._nb_cases_l,1, \
		self._nb_cases_h)
		tab_carte_objets=LoadIntFromFile(id_carte+"objets.csv",1,self._nb_cases_l,1, \
		self._nb_cases_h)
		self._cases =  [[ Case( (j,j), tab_carte_objets[i][j], tab_carte[i][j] ) for j in\
		 range(self._nb_cases_h)] for i in range(self._nb_cases_l)]
		dico_nom_id=DicoFromFile("cartes_legend2.csv",2,16,1,0)
		dico_name_to_id_graph=DicoFromFile("cartes_legend2.csv",2,16,1,2)
		for i in range(0,self.nb_cases_l):
			for j in range(0,self._nb_cases_h):
				ob = tab_carte_objets[i][j]
				if(dico_nom_id[ob]=="source"):
					self._cases[i][j]  =   Source((j,i),tab_carte[i][j],ob)
					self._pos_sources.append((j, i))
				elif dico_nom_id[ob]=="base":
					self._cases[i][j] = Base((j,i),tab_carte[i][j],ob)
					self._pos_bases.append((j,i))
				elif dico_nom_id[ob]=="place_construction":
					self._cases[i][j]= Emplacement((j,i),tab_carte[i][j],ob)
				chemin = tab_carte[i][j]
				if(chemin==1):
					self._cases[i][j]._est_chemin=chemin;
					self._cases[i][j]._tapis = 1;
					self.set_cout_case((j,i),1)
		# for x in range(0,self.nb_cases_h):
		# 	for y in range(0,self._nb_cases_l):
		# 		print((x,y) , (x,y) in self )

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


	def set_chemin(self, (x,y), value):
		self[y][x].est_chemin = value

	def __contains__(self, position):
	    col, lig = position
	    return (lig >= 0) and (lig < self._nb_cases_l) and (col >= 0) \
		and (col < self._nb_cases_h)

	def __getitem__(self, col, lig):
		if (lig,col) in self:
			return self._cases[lig][col]

	def __getitem__(self, position):
		col, lig = position
		if position in self:
			return self._cases[lig][col]
		else:
			print("error")

	def set_case(self, position, valeur):
		self[position]= valeur

	def __setitem__(self, position, valeur):
		col, lig = position
		# print("i am the setter hello")
		if position in self:
			self._cases[lig][col] = valeur

# Getteur setter des cout
	def get_cout_chemin(self,(pos_x,pos_y)):
		return self._cout_chemin[pos_y][pos_x]

	def get_cout_case(self,(pos_x,pos_y)):
		return self._cout_case[pos_y][pos_x]

	def set_cout_chemin(self,(pos_x,pos_y),cout):
		self._cout_chemin[pos_y][pos_x] = cout;

	def set_cout_case(self,(pos_x,pos_y),cout):
		self._cout_case[pos_y][pos_x] = cout;

	def objet_dans_case(self, objet_position):
		""" Retourne les coordonnées de la case de l'objet """
		pas_l = int(self.largeur/self.nb_cases_h)
		pas_h = int(self.hauteur/self.nb_cases_l)
		a = int(objet_position[0]*self._nb_cases_h/self._largeur)
		b = int(objet_position[1]*self._nb_cases_l/self._hauteur)
		return (a,b)

	def positionner_objet(self, pos_case):
		a = int(pos_case[0]*self.largeur/self.nb_cases_h)+1
		b = int(pos_case[1]*self.hauteur/self.nb_cases_l)+1
		return (a, b)

	def genere_decor(self,tab_objet):
		max_ligne_tab_objet=max([tab_objet[j] for j in range(len(tab_objet))])
		tab_carte_objets=LoadIntFromFile(self._id_carte+"objets.csv",1, \
		max_ligne_tab_objet,1,len(tab_objet))
		for j in range(len(tab_objet)):
			for i in range(tab_objet[j]):
				x, y = np.random.randint(self.nb_cases_h-1), np.random.randint(1,\
				 self.nb_cases_l-1)
				while self[(x,y)]._tapis!=0 and self.get_type_case((x,y))!=\
				"place_construction":
					print(self.get_type_case((x,y)))
					x, y = np.random.randint(self.nb_cases_h-1), np.random.randint(\
					self.nb_cases_l-1)
				self[(x,y)] = Element_decor((x,y),1000+j+1,0)

#@getter et setter
	# def get_case(self,i,j):
	# 	return self._cases[i][j]
	#
	# def get_case(self,pos):
	# 	return self[pos[1]][pos[0]]

	def get_type_case(self, pos):
		return self[pos]._type_objet

	def get_base(self,i):
		return self[self._pos_bases[i]]

	def get_source(self,i):
		return self[self._pos_sources[i]]

	def est_case_chemin(self,pos,soldat_direction=0):
		if  (pos[0]>=self.nb_cases_h) or (pos[1]>=self.nb_cases_l) or (pos[0]<0)or \
		(pos[1]<0):
			return False
		else:
			return self[pos].est_chemin(soldat_direction)

	def actualise(self):
		# print("on rentre dans a=la fonction de mise à jour de la carte")
		#on met à jour la liste des tours
		#mise à jour de la carte des couts liée aux tours
		for pos in self._pos_bases:
			if(self[pos].actualisation()):
				self.base_est_morte(pos)
				self.actualise_cout_chemin()
		for x in range(self._nb_cases_h):
			for y in range(self._nb_cases_l):
				self[(x,y)].actualisation()

#Gestion de la carte de cout
	def rec_actualise_cout_chemin(self, pos_case, vect_voisin, cout_actuel):
		self.set_cout_chemin(pos_case, cout_actuel)
		for i in range( len(vect_voisin)):
			#le soldat va dans l'autre sens et est tourné dans le sens opposé
			direction = i+2%4
			voisin = vect_voisin[i]
			tmp_a, tmp_b = (pos_case[0]+voisin[0]), (pos_case[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			if(case_voisin in self):
				if (self.est_case_chemin(case_voisin,direction)) and \
				(self.get_cout_case(case_voisin) + self.get_cout_chemin(pos_case) < \
				self.get_cout_chemin(case_voisin)):
					new_cost = self.get_cout_case(case_voisin) + \
					self.get_cout_chemin(pos_case)
					self.rec_actualise_cout_chemin(case_voisin, vect_voisin, new_cost )

	def reinitialiser_cout_case(self):
		for i in range(self._nb_cases_h):
			for j in range(self._nb_cases_l):
				self._cout_case[j][i] = 1

	def reinitialiser_cout_chemin(self):
		for i in range(self._nb_cases_h):
			for j in range(self._nb_cases_l):
				self._cout_chemin[j][i] = float('inf')

	def actualise_cout_chemin(self):
		self.reinitialiser_cout_chemin()
		voisin = [(0, 1), (-1,0), (0, -1), (1, 0)]
		for i,pos_base in enumerate(self._pos_bases):
			if(not self.get_base(i)._est_mort):
				self.rec_actualise_cout_chemin(pos_base, voisin, 1 )
		# affiche_tableau(self._cout_case)
		# affiche_tableau(self._cout_chemin)


#Gestion des sources et des bases

	def base_est_morte(self, pos):
		dico_dir_vers_entier = { (0,1) : -3 , (0,-1) : -1 , (1,0) : -2 , (-1,0) : -4}
		old_pos = pos
		pos_act = pos
		voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]
		liste_voisins =[]
		for voisin in voisins:
			tmp_a, tmp_b = int(pos_act[0]+voisin[0]), int(pos_act[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			if(case_voisin in self):
				if self.est_case_chemin(case_voisin) and case_voisin != old_pos:
					liste_voisins.append(case_voisin)
		if(len(liste_voisins)==1):
			while len(liste_voisins)<=1:
				liste_voisins =[]
				for voisin in voisins:
					tmp_a, tmp_b = int(pos_act[0]+voisin[0]), int(pos_act[1]+voisin[1])
					case_voisin = (tmp_a, tmp_b)
					if(case_voisin in self):
						if self.est_case_chemin(case_voisin) and case_voisin != old_pos:
							liste_voisins.append(case_voisin)
				if(len(liste_voisins)==0):
					print("la carte est une ligne droite non ?")
					return 0
				if(len(liste_voisins)==1):
					old_pos = pos_act
					pos_act=liste_voisins[0]
			direction = (old_pos[0]-pos_act[0],old_pos[1]-pos_act[1])
			self[old_pos]._est_chemin = dico_dir_vers_entier[direction]
		else :
			None

	def initialiser_source(self, i):
		pos_case = self._pos_sources[i]
		source = self.get_source(i)
		voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]
		for i,voisin in enumerate(voisins):
			tmp_a, tmp_b = (pos_case[0]+voisin[0]), (pos_case[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			assert(case_voisin != (source._position))
			if(case_voisin in self):
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


	def get_voisins_case(self,pos, liste_voisin, old_pos = (-50,-50)):
		assert(len(liste_voisin)==0)
		voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]
		for voisin in voisins:
			tmp_a, tmp_b = int(pos_act[0]+voisin[0]), int(pos_act[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			if(case_voisin in self):
				if self.est_case_chemin(case_voisin) and case_voisin != old_pos:
					liste_voisins.append(case_voisin)

	#fonction qui met à jour la liste des tours dans la carte
	# def miseajourliste_tours(self):
	# 	for x in range(0,self.nb_cases_h):
	# 		for y in range(0,self._nb_cases_l):
	# 			# print(" on rentre dans la fonction mise a jour des listes de tours")
	# 			if((self[(x,y)].type_objet=="tour") and (self[x,y] not in \
	# 			self._liste_tours_actuelle) ):
	# 				self._liste_tours_a_actualise.append((self[x,y],(x,y)))
	#
	# #permet de mettre à jour la carte des couts en fonction des bases
