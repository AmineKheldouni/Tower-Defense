#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *

# AJOUTER LA CLASSE ARMEE ET SOLDAT PUIS LA CLASSE PROJECTILE
class Soldat:
	def __init__(self, position, joueur, position_base, rang_soldat=0, vie=10, vitesse=(1,0), degat=3, valeur_soldat=10):
		""" Les champs position et vitesse sont deux vecteurs de composantes x et y
	    valeur_soldat correspond à la valeur que le joueur obtient s'il l'élimine"""

		self._type_soldat = rang_soldat
		self._vie = vie
		self._vitesse = vitesse
		self._position = position
		self._degat = degat
		self._valeur_soldat = valeur_soldat	# Score du joueur en tuant ce type de soldat
		self._direction = 2 # 0 : bas, 1 : gauche, 2 : haut, 3 : droite
		self._animation = 0 # 0 : statique 1 : pied droit 2 : pied gauche
		self._joueur = joueur
		self._position_objectifs= self._joueur._carte.positionner_objet(position_base)
		self.pas = 25.
		self._voisins = [(0, int(self.pas)), (-int(self.pas),0), (0, -int(self.pas)), (int(self.pas), 0)] # FAIRE UN DICTIONNAIRE
	@property
	def vie(self):
		return self._vie

	def vitesse(self):
	    return self._vitesse

	def position(self):
	    return self._position

	def degat(self):
	    return self._degat

	def valeur_soldat(self):
	    return self._valeur_soldat

	def miseajourscore(self,joueur):
	    """
	    mise à jour du score du joueur en cas d'élimination du soldat
	    """
	    if (self.vie == 0):
	        joueur._score+=self.valeur_soldat

	def deplacement_soldat(self):
	    tmp_x = self._vitesse[0] + self._position[0]
	    tmp_y = self._vitesse[1] + self._position[1]
	    self._position = tmp_x, tmp_y
	    self._animation += 1
	    if self._animation == 3:
			self._animation = 0

	def voisins_chemin(self):
		pos_soldat = self._position
		case_soldat = self._joueur._carte.objet_dans_case(pos_soldat)
		liste_voisins_chemin = []
		liste_distance = []
		for voisin in self._voisins:
			tmp_a, tmp_b = int(case_soldat[0]+voisin[0]/self.pas), int(case_soldat[1]+voisin[1]/self.pas)
			case_voisin = (tmp_a, tmp_b)
			if self._joueur._carte[case_voisin] == "chemin":
				liste_voisins_chemin.append(voisin)
				pos_voisin = self._joueur._carte.positionner_objet(case_voisin)
				dist_tmp = abs(pos_voisin[0]-self._position_objectifs[0])+abs(pos_voisin[1]-self._position_objectifs[1])
				liste_distance.append(dist_tmp)
			print("Liste voisins chemin : ", liste_voisins_chemin)
			print("Liste distances : ", liste_distance)
		for i in range(len(liste_voisins_chemin)):
			if liste_distance[i] == min(liste_distance):
				return liste_voisins_chemin[i]

	def maj_direction(self):
		pos_soldat = self._position
		case_soldat = self._joueur._carte.objet_dans_case(pos_soldat)
		pos_tmp = self._joueur._carte.positionner_objet(case_soldat)
		if pos_soldat == pos_tmp:
			meilleur_voisin = self.voisins_chemin()
			self._direction = self._voisins.index(meilleur_voisin)
	#A Faire: fonction de gestion du mouvement du soldat en fonction de sa distance à la base et du chemin


class Armee:
	def __init__(self, tableau_soldat, joueur):
		self._taille_effectif = len(tableau_soldat)
		self._liste_soldat = tableau_soldat
		self._joueur = joueur

	@property
	def joueur(self):
		return self._joueur

	def mouvement_troupe(self):
		assert(self._taille_effectif != 0)
		for soldat in self._liste_soldat:
			for i in range(4):
				if soldat._direction == i:
					soldat._vitesse = soldat._voisins[i]
					soldat_copy = copy.deepcopy(soldat)
					soldat_copy.deplacement_soldat()
					if (self._joueur._carte[self._joueur._carte.objet_dans_case(soldat_copy._position)] == "chemin"):
						soldat.deplacement_soldat()
			soldat.maj_direction()
