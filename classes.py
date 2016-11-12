#!/usr/bin/python
#encoding: utf8
import pygame
from pygame.locals import *

import functools
from functools import partial
import copy
import sys
import numpy as np


class Carte:
	def __init__(self, hauteur=800, largeur=1000, nb_cases_h = 16, \
	nb_cases_l = 20):
		self._hauteur = hauteur
		self._largeur = largeur
		self._nb_cases_h = nb_cases_h
		self._nb_cases_l = nb_cases_l
		self._grille = [[5 for i in range(self._nb_cases_l)] for j in range(self._nb_cases_h)] # 5 = Case libre (verdure)
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

class Joueur:
	def __init__(self, carte, argent = 50, score = 0):
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



class Affichage_fenetre:
	def __init__(self, carte, joueur):
		self._liste_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._liste_soldats = ["images/armee/soldat1.png"]
		self._carte = carte
		self._fenetre = pygame.display.set_mode((self._carte._largeur, self._carte._hauteur))
		self._nb_decor = [10, 15] # 10 Rochers, 5 Arbres
		self._joueur = joueur
		self._bases = [Base(((self._carte._nb_cases_l-1)*self._carte._largeur/self._carte._nb_cases_l, self._carte._hauteur/self._carte._nb_cases_h*(self._carte._nb_cases_h//2)), self._carte)]
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
		# Affichage décor :
		for i in range(self._nb_decor[0]):
			pos_x = np.random.randint(self._carte._nb_cases_l) * self._carte._largeur/self._carte._nb_cases_l
			pos_y = np.random.randint(self._carte._nb_cases_h) * self._carte._hauteur/self._carte._nb_cases_h
			while (pos_x, pos_y) in self._carte and self._carte[pos_x, pos_y] != 5:
				pos_x = np.random.randint(self._carte._nb_cases_l)
				pos_y = np.random.randint(self._carte._nb_cases_h)
				print pos_x, pos_y
			self._carte[pos_x, pos_y] = 1 # La case devient un decor
			self.ajouter_element("images/interface/rock.png", (pos_x, pos_y))
		for i in range(self._nb_decor[1]):
			pos_x = np.random.randint(self._carte._nb_cases_l) * self._carte._largeur/self._carte._nb_cases_l
			pos_y = np.random.randint(1, self._carte._nb_cases_h) * self._carte._hauteur/self._carte._nb_cases_h
			while (pos_x, pos_y) in self._carte and self._carte[pos_x, pos_y] != 5:
				pos_x = np.random.randint(self._carte._nb_cases_l)
				pos_y = np.random.randint(self._carte._nb_cases_h)
			self._carte[pos_x, pos_y] = 1 # La case devient un decor
			self.ajouter_element("images/interface/arbre.png", (pos_x, pos_y))
		# Affichage chemin :

		# Affichage bases :
		for b in self._bases:
			self.ajouter_element("images/interface/base.png", b._position)

		# Affichage place de construction : A COMPLETER !
			tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l), np.random.randint(self._carte._nb_cases_h)
			pos_x = tmp1 * self._carte._largeur/self._carte._nb_cases_l
			pos_y = tmp2 * self._carte._hauteur/self._carte._nb_cases_h
			while (pos_x, pos_y) in self._carte and self._carte[pos_x, pos_y] != 5:
				tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l), np.random.randint(self._carte._nb_cases_h)
				pos_x = tmp1 * self._carte._largeur/self._carte._nb_cases_l
				pos_y = tmp2 * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[tmp1, tmp2] = 2 # La case devient une place de construction
			print "Place_construction : ", tmp1, tmp2
			self.ajouter_element("images/interface/place_construction.png", (pos_x, pos_y))

	def affichage_tours(self):
		for T in self._joueur._liste_tours:
			self.ajouter_element(self._liste_tours[T._id_tour], T._position)
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
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			J.construit_tour(event)
			F.affichage_tours()
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer = 0      #On arrête la boucle


if __name__ == '__main__':
    main()
