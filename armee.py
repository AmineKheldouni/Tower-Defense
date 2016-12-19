#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *

# AJOUTER LA CLASSE ARMEE ET SOLDAT PUIS LA CLASSE PROJECTILE
class Soldat:
	def __init__(self, position, joueur, id_soldat=1):
		""" Les champs position et vitesse sont deux vecteurs de composantes x et y
	    valeur_soldat correspond à la valeur que le joueur obtient s'il l'élimine"""

		self._type_soldat   = extract("armee",id_soldat,0)
		self._vie           = extract("armee",id_soldat,2)
		self._vitesse       = extract("armee",id_soldat,4)
		self._degat         = extract("armee",id_soldat,5)
		self._valeur_soldat = extract("armee",id_soldat,6)	# Score du joueur en tuant ce type de soldat
		self._graphic       = extract_string("armee",id_soldat,7)

		self.pos_init = position
		self._joueur = joueur
		self._position = position
		self._ancienne_position = self._position
		self._is_dead = False
		self._direction = 2 # 0 : bas, 1 : gauche, 2 : haut, 3 : droite
		self._animation = 0 # 0 : statique 1 : pied droit 2 : pied gauche
		# self._position_objectifs= self._joueur._carte.positionner_objet(position_base)
		self._pas = 1.
		self._voisins = [(0, int(self.pas)), (-int(self.pas),0), (0, -int(self.pas)), (int(self.pas), 0)] # FAIRE UN DICTIONNAIRE
		self._chemin = []
		self.liste_voisins = []
		self.liste_vitesses = []
		self._est_mort = False

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

	def miseajourscore(self,joueur):
	    """
	    mise à jour du score du joueur en cas d'élimination du soldat
	    """
	    if (self.vie == 0):
	        joueur._score += self.valeur_soldat

	def deplacement_soldat(self, dt):
	    tmp_x = self._vitesse[0]*dt + self._position[0]
	    tmp_y = self._vitesse[1]*dt + self._position[1]
	    self._position = tmp_x, tmp_y
	    self._animation += 1
	    if self._animation == 3:
			self._animation = 0

	def arriver_base(self):
		pos_case = self._joueur._carte.objet_dans_case(self._position)
		if self._joueur.carte.get_type_case(pos_case) == "base":
			self._joueur.carte._cases[pos_case[0]][pos_case[1]].dommage(self._degat)
			self._est_mort = True
			return True
		return False

	def maj_direction(self, dt):
		# A MODIFIER
		pos_case = self._joueur._carte.objet_dans_case(self._position)
		choix_voisin = None
		self.liste_voisins = []
		self.liste_vitesses = []
		for voisin in self._voisins:
			tmp_a, tmp_b = int(pos_case[0]+voisin[0]/self.pas), int(pos_case[1]+voisin[1]/self.pas)
			case_voisin = (tmp_a, tmp_b)
			if (self._joueur._carte.est_case_chemin(case_voisin)) and case_voisin not in self.liste_voisins and case_voisin != self._joueur._carte.objet_dans_case(self.pos_init) and case_voisin != self._joueur.carte.objet_dans_case(self._ancienne_position) :
				self.liste_voisins.append(case_voisin)
				self.liste_vitesses.append(voisin)
		for i in range(len(self.liste_voisins)):
			for j in range(len(self.liste_voisins)):
				choix_voisin = self.liste_voisins[0], self.liste_vitesses[0]
				if len(self.liste_voisins) == 2:
					pos_case = self._joueur._carte.objet_dans_case(self._position)
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
			self._vitesse = choix_voisin[1]
			self._ancienne_position = self._position
			while self._position != self._joueur._carte.positionner_objet(choix_voisin[0]):
				self.deplacement_soldat(dt)

	def maj_direction2(self, dt):
		pos_case = self._joueur._carte.objet_dans_case(self._position)
		choix_voisin = None
		self.liste_voisins = []
		self.liste_vitesses = []
		for voisin in self._voisins:
			tmp_a, tmp_b = int(pos_case[0]+voisin[0]/self.pas), int(pos_case[1]+voisin[1]/self.pas)
			case_voisin = (tmp_a, tmp_b)
			if (self._joueur._carte.est_chemin(case_voisin)) and case_voisin not in self.liste_voisins and case_voisin != self._joueur._carte.objet_dans_case(self.pos_init) and case_voisin != self._joueur.carte.objet_dans_case(self._ancienne_position) :
				self.liste_voisins.append(case_voisin)
				self.liste_vitesses.append(voisin)
			else:
					choix_voisin = self.liste_voisins[0], self.liste_vitesses[0]
		if choix_voisin != None:
			self._direction = self._voisins.index(choix_voisin[1])
			self._vitesse = choix_voisin[1]
			self._ancienne_position = self._position
			while self._position != self._joueur._carte.positionner_objet(choix_voisin[0]):
				self.deplacement_soldat(dt)

	def dir_to_graph(self):
		dir_vect=["_bas","_gauche","_haut","_droite"]
		dir_anim=["","_pd","_pg"]
		return dir_vect[self._direction]+dir_anim[self._animation]

class Armee:
	def __init__(self, tableau_soldat, joueur):
		self._taille_effectif = len(tableau_soldat)
		self._liste_soldat = tableau_soldat
		self._joueur = joueur

	@property
	def joueur(self):
		return self._joueur

	def mouvement_troupe(self, dt):
		assert(self._taille_effectif != 0)
		soldats_arrives = []
		for i in range(len(self._liste_soldat)):
			soldat = self._liste_soldat[i]
			soldat.maj_direction(dt)
			if soldat.arriver_base():
				soldats_arrives.append(i)
		for i in soldats_arrives:
                        #assert erreur index out of range
                        assert(i<len(self._liste_soldat))
			del self._liste_soldat[i]


	def maj_troupe(self):
		liste_morts = []
		for i in range(len(self._liste_soldat)):
			self._liste_soldat[i].miseajourscore(self._joueur)
			if self._liste_soldat[i].vie == 0:
				liste_morts.append(i)
		for idx in liste_morts:
			del self._liste_soldat[idx]
