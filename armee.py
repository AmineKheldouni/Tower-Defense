#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *

# AJOUTER LA CLASSE ARMEE ET SOLDAT PUIS LA CLASSE PROJECTILE
class Soldat:
	def __init__(self, position, rang_soldat=0, vie=10, vitesse=(1,0), degat=3, valeur_soldat=10):
		""" Les champs position et vitesse sont deux vecteurs de composantes x et y
	    valeur_soldat correspond à la valeur que le joueur obtient s'il l'élimine"""

		self._type_soldat = rang_soldat
		self._vie = vie
		self._vitesse = vitesse
		self._position = position
		self._degat = degat
		self._valeur_soldat = valeur_soldat	# Score du joueur en tuant ce type de soldat
		self._direction = 0 # 0 : bas, 1 : gauche, 2 : haut, 3 : droite

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

	#A Faire: fonction de gestion du mouvement du soldat en fonction de sa distance à la base et du chemin


class Armee:
    def __init__(self, tableau_soldat, position_base, carte):
		self._taille_effectif = len(tableau_soldat)
		self._liste_soldat = tableau_soldat
		self._carte = carte
        #position des bases
		self._position_objectifs=position_base
		self._voisins = [(0, 10), (-10,0), (0, -10), (10, 0)] # FAIRE UN DICTIONNAIRE
    # Faire la gestion du mouvement des troupes

    def mouvement_troupe(self):
		assert(self._taille_effectif != 0)
		pos = self._liste_soldat[0]._position
		dist_base = m.sqrt((pos[0]-self._position_objectifs[0])**2+(pos[1]-self._position_objectifs[1])**2)
		meilleur_voisin = (0, 0)
		for voisin in self._voisins:
			if self._carte[pos[0]+voisin[0], pos[1]+voisin[1]] != 4 and self._carte[pos[0]+voisin[0], pos[1]+voisin[1]] != 1:
				dist_base2 = m.sqrt((pos[0]+voisin[0]-self._position_objectifs[0])**2+(pos[1]+voisin[1]-self._position_objectifs[1])**2)
				if dist_base2 <= dist_base:
					meilleur_voisin = voisin
					dist_base = dist_base2
		for soldat in self._liste_soldat:
			for i in range(len(self._voisins)):
				if self._voisins[i][0] == meilleur_voisin[0] and self._voisins[i][1] == meilleur_voisin[1]:
					soldat._direction = i
			soldat._vitesse = meilleur_voisin
			soldat.deplacement_soldat()
