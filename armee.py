#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from objet_actif import *

# AJOUTER LA CLASSE ARMEE ET SOLDAT PUIS LA CLASSE PROJECTILE
class Soldat(Objet_Actif):
	def __init__(self, position, id_soldat=1):
		super(Soldat,self).__init__(position,"soldat",id_soldat)
		""" Les champs position et vitesse sont deux vecteurs de composantes x et y
	    valeur_soldat correspond à la valeur que le joueur obtient s'il l'élimine"""
		self._type_soldat   = extract("armee",id_soldat,0)
		self._vie           = extract("armee",id_soldat,2)
		self._vitesse       = extract("armee",id_soldat,4)
		self._degat         = extract("armee",id_soldat,5)
		self._valeur_soldat = extract("armee",id_soldat,6)	# Score du joueur en tuant ce type de soldat
		self._argent_soldat = extract("armee",id_soldat,7)
		self._graphic       = extract_string("armee",id_soldat,8)

		self._position = position
		self._ancienne_position = position
		self._is_dead = False
		self._direction = 2 # 0 : bas, 1 : gauche, 2 : haut, 3 : droite
		self._animation = 0 # 0 : statique 1 : pied droit 2 : pied gauche
		self._pas = 0 #position dans la case
		self._value_case = 100 #valeur d'une case
		self._voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]
		self.liste_voisins = []
		self.liste_vitesses = []

	@property
	def vie(self):
		return self._vie

	@property
	def vitesse(self):
	    return self._vitesse

	@property
	def position(self):
	    return self._position

	@property
	def degat(self):
	    return self._degat

	@property
	def valeur_soldat(self):
	    return self._valeur_soldat
	@property
	def pas(self):
		return self._pas

	def deplacement_soldat(self,carte):
		self._pas = self._pas + self._vitesse
		self.anime()
		if(self._pas >= self._value_case):
			self._pas-=self._value_case
			self.maj_direction2(carte)

	def arriver_base(self,carte):
		pos_case = self._position
		if carte.get_type_case(pos_case) == "base":
			carte._cases[pos_case[0]][pos_case[1]].dommage(self._degat)
			self.meurt()
			return True
		return False

	def maj_direction2(self,carte):
		# A MODIFIER
		pos_case = self._position
		choix_voisin = None
		self.liste_voisins = []
		self.liste_vitesses = []
		for voisin in self._voisins:
			tmp_a, tmp_b = int(pos_case[0]+voisin[0]), int(pos_case[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			if (carte.est_case_chemin(case_voisin,self._direction)) and case_voisin != (self._position) and case_voisin != (self._ancienne_position):
				self.liste_voisins.append(case_voisin)
				self.liste_vitesses.append(voisin)
		for i in range(len(self.liste_voisins)):
			for j in range(len(self.liste_voisins)):
				choix_voisin = self.liste_voisins[0], self.liste_vitesses[0]
				if len(self.liste_voisins) == 2:
					pos_case = self._position
					if self.liste_voisins[0][1] > self.liste_voisins[1][1]:
						choix_voisin = self.liste_voisins[1], self.liste_vitesses[1]
					if self.liste_voisins[0][1] < self.liste_voisins[1][1]:
						choix_voisin = self.liste_voisins[0], self.liste_vitesses[0]
					if self.liste_voisins[0][1] == self.liste_voisins[1][1] or \
					(self.liste_voisins[0][1] < self.liste_voisins[1][1] and \
					self.liste_voisins[1][1] == pos_case[1]) or  \
					(self.liste_voisins[1][1] < self.liste_voisins[0][1] and \
					self.liste_voisins[0][1] == pos_case[1]):
						p = rd.randint(0, 2)
						choix_voisin = self.liste_voisins[p], self.liste_vitesses[p]
		if choix_voisin != None:
			self._direction = self._voisins.index(choix_voisin[1])
			self._ancienne_position = self._position
			self._position= choix_voisin[0]


	def dir_to_graph(self):
		dir_vect=["_bas","_gauche","_haut","_droite"]
		dir_anim=["","_pd","_pg"]
		return dir_vect[self._direction]+dir_anim[self._animation]

	def anime(self):
		self._animation += 1
		if self._animation == 3:
			self._animation = 0

	def actualisation(self):
		self.actualise_etat()

class Armee:
	def __init__(self, tableau_soldat):
		self._taille_effectif = len(tableau_soldat)
		self._liste_soldat = tableau_soldat

	def mouvement_troupe(self,carte):
		assert(self._taille_effectif != 0)
		soldats_arrives = []
		for i in range(len(self._liste_soldat)):
			soldat = self._liste_soldat[i]
			soldat.actualisation()
			soldat.deplacement_soldat(carte)
		# 	if soldat.arriver_base(carte):
		# 		soldats_arrives.append(i)
		# for i in soldats_arrives:
        #                 #assert erreur index out of range
        #                 assert(i<len(self._liste_soldat))
		# 	del self._liste_soldat[i]

	def maj_troupe(self):
		liste_morts = []
		argent = 0
		point  = 0
		for i in range(len(self._liste_soldat)):
			if (self._liste_soldat[i]).est_mort():
				liste_morts.append(i)
				argent+=self._liste_soldat[i]._argent_soldat
				point +=self._liste_soldat[i]._valeur
		for idx in liste_morts:
			del self._liste_soldat[idx]
		return(argent,valeur)
