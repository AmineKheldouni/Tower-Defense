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
		self._grille = [[5 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)] # 5 = Case libre (verdure)
		self._carte_couts = [10000]
		self._liste_construction = []
		self._liste_chemin = []
		self._liste_tour = []
		self._liste_bases = [((nb_cases_l-1)*largeur/nb_cases_l, hauteur/nb_cases_h*(nb_cases_h//2))]
		self._liste_decor = []

	@property
	def carte_couts(self):
		return self._carte_couts

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
				if objet_position[0]-i*self._largeur/self._nb_cases_l >=0 and \
				objet_position[0]-i*self._largeur/self._nb_cases_l < self._largeur/self._nb_cases_l \
				and objet_position[1]-j*self._hauteur/self._nb_cases_h >=0 and \
				objet_position[1]-j*self._hauteur/self._nb_cases_h < self._hauteur/self._nb_cases_h:
					return i, j

	def case_construction(self, i, j):
		self._liste_construction.append((i, j))
		self._grille[i, j] = 2


	def case_chemin(self, i, j):
		self._liste_chemin.append((i, j))
		self._grille[i, j] = 0 # La case est un chemin

	def case_chemin(self, i, j):
		self._liste_tour.append((i, j))
		self._grille[i, j] = 3 # La case est une tour

	def case_decor(self, i, j):
		self._liste_decor.append((i, j))
		self._grille[i, j] = 4 # La case est un rocher/arbre


class Base:
	def __init__(self, position, carte, cout_entretien=100,\
	 cout_amelioration=20, hp = 1):
		self._vie = hp
		self._carte = carte
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._position = position
		self._carte[position] = 6 # 6 = base

	@property
	def vie(self):
		return self._vie
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

class Tour:
	def __init__(self, position, projectile,hp = 10, portee = 400, cout_construction=10, \
	cout_entretien=2, cout_amelioration = 50, id_tour=1):
		self._projectile = projectile
		self._vie = hp
		self._portee = portee
		self._cout_construction = cout_construction
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._id_tour = id_tour
		self._position = position
	# A COMPLETER

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
	    """
	     mise à jour de la position du soldat avec le champs vitesse
	     """
	    (vx,vy) = self.vitesse
	    self.position[0] += vx
	    self.position[1] += vy

	#A Faire: fonction de gestion du mouvement du soldat en fonction de sa distance à la base et du chemin


class Armee:
    def __init__(self,tableau_soldat,position_base):
        self._taille_effectif = len(tableau_soldat)
        self._liste_soldat = tableau_soldat
        #position des bases
        self._position_objectifs=position_base
    # Faire la gestion du mouvement des troupes




class Joueur:
	def __init__(self, carte, argent = 10, score = 0):
		self._argent = argent
		self._score = score
		self._liste_tours = []
		self._carte = carte
	def construit_tour(self, event):
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				pos_x, pos_y = self._carte.objet_dans_case(event.pos)
				if self._carte[pos_x, pos_y] == 2:
					pos_pix = pos_x*self._carte._largeur/self._carte._nb_cases_l\
					, pos_y*self._carte._hauteur/self._carte._nb_cases_h
					T = Tour(pos_pix, 1)
					if T._cout_construction <= self._argent:
						self._liste_tours.append(T)
						self._argent -= T._cout_construction
						self._carte[pos_x, pos_y] = 10
					else:
						print "Vous n'avez pas suffisamment d'argent."

class Affichage_fenetre:
	def __init__(self, carte, joueur):
		self._liste_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._liste_soldats = ["images/armee/boss/boss_bas.png"]
		self._carte = carte
		self._fenetre = pygame.display.set_mode((self._carte._largeur, self._carte._hauteur))
		self._nb_decor = [10, 15] # 10 Rochers, 5 Arbres
		self._joueur = joueur
		self._bases = [Base(((self._carte._nb_cases_l-1)*self._carte._largeur/self._carte._nb_cases_l, self._carte._hauteur/self._carte._nb_cases_h*(self._carte._nb_cases_h//2)), self._carte)]
		self._places_construction = [(10,10), (15, 10), (3, 2)]
	def ajouter_element(self, nom_image, position):
		element = pygame.image.load(nom_image).convert_alpha()
		if "tour" in nom_image or "arbre" in nom_image:
			self._fenetre.blit(element, (position[0], position[1]-\
			self._carte._hauteur/self._carte._nb_cases_h))
		else:
			self._fenetre.blit(element, position)

	def affichage_statique(self):
		""" Reorganiser la fonction pour éviter la duplication de code ! """
		self.ajouter_element("images/interface/background2.jpg", (0, 0))
		# Affichage place de construction : A COMPLETER !
		for pc in self._places_construction:
			pos_x = pc[0] * self._carte._largeur/self._carte._nb_cases_l
			pos_y = pc[1] * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[pc] = 2 # La case devient une place de construction
			self.ajouter_element("images/interface/place_construction.png", (pos_x, pos_y))

		# Affichage décor :
		for i in range(self._nb_decor[0]):
			tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			while self._carte[tmp1, tmp2] != 5:
				tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			pos_x = tmp1 * self._carte._largeur/self._carte._nb_cases_l
			pos_y = tmp2 * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[tmp1, tmp2] = 1 # La case devient un decor
			self.ajouter_element("images/interface/rock.png", (pos_x, pos_y))
		for i in range(self._nb_decor[1]):
			tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			while self._carte[tmp1, tmp2] != 5:
				tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			pos_x = tmp1 * self._carte._largeur/self._carte._nb_cases_l
			pos_y = tmp2 * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[tmp1, tmp2] = 1 # La case devient un decor
			self.ajouter_element("images/interface/arbre.png", (pos_x, pos_y))
		# Affichage chemin :
		source = (0, self._carte._hauteur/2)
		tmp_case = source
		chemin = [source]
		self._carte[source] = 1
		"""pas_l = self._carte._largeur/self._carte._nb_cases_l
		pas_h = self._carte._hauteur/self._carte._nb_cases_h
		cases_voisines = [(-pas_l,0), (pas_l, 0), (0, -pas_h), (0, pas_h)]
		for b in self._bases:
			dist_base = m.sqrt((tmp_case[0]-b._position[0])**2+(tmp_case[1]-b._position[1])**2)
			while tmp_case != b.position:
				meilleur_voisin = tmp_case
				min_dist = dist_base
				for voisin in cases_voisines:
					tmp_case2 = tmp_case[0]+voisin[0], tmp_case[1]+voisin[1]
					dist_base2 = m.sqrt((tmp_case2[0]-b._position[0])*\
					(tmp_case2[0]-b._position[0])+(tmp_case2[1]-b._position[1])\
					*(tmp_case2[1]-b._position[1]))
					if self._carte[tmp_case2] == 5:
						if dist_base2 <= dist_base:
							meilleur_voisin = tmp_case2
							min_dist = dist_base2
				self._carte[meilleur_voisin] = 1
				chemin.append(meilleur_voisin)"""

		for position_chemin in chemin:
			self.ajouter_element("images/interface/route.jpg", position_chemin)


		# Affichage bases :
		for b in self._bases:
			self.ajouter_element("images/interface/base.png", b._position)

	def affichage_tours(self):
		for T in self._joueur._liste_tours:
			self.ajouter_element(self._liste_tours[T._id_tour], T._position)

	def affichage_armee(self):
		for b in self._bases:
			S = Soldat((0, self._carte._hauteur/2))
			A = Armee([S], b._position)
			for soldat in A._liste_soldat:
				type_soldat = soldat._type_soldat
				self.ajouter_element(self._liste_soldats[type_soldat], soldat._position)
def main():
	pygame.init()

	#Ouverture de la fenêtre Pygame
	C = Carte()
	J = Joueur(C)
	F = Affichage_fenetre(C, J)
	continuer = 1
	#Chargement et collage du fond
	F.affichage_statique()
	F.affichage_tours()
	pygame.display.flip()
	#Boucle infinie
	while continuer:
		pygame.display.flip()
		F.affichage_armee()
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			J.construit_tour(event)
			F.affichage_tours()
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer = 0      #On arrête la boucle

if __name__ == '__main__':
    main()
