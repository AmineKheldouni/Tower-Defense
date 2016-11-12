#!/usr/bin/python
#encoding: utf8
import pygame
from pygame.locals import *

import functools
from functools import partial
import copy
import sys

class Carte:
	def __init__(self, hauteur=600, largeur=800, pas=50):
		self._hauteur = hauteur
		self._largeur = largeur
		self._pas = pas
		self._grille = [[1 for i in range(largeur)] for j in range(hauteur)]
		self._carte_couts = [10000]
		self._liste_cases_construction = []
		self._liste_cases_chemin = []
		self._liste_cases_tour = []
		self._liste_cases_bases = [(hauteur*hauteur/(2*pas), largeur-largeur/pas)]
		self._liste_cases_decor = []

	@property
	def carte_couts(self):
		return self._carte_couts

	def __contains__(self, position):
	    lig, col = position
	    return (lig >= 0) and (lig < self._largeur) and (col >= 0) \
		and (col < self._hauteur)

	def __getitem__(self, position):
		lig, col = position
		if position in self:
			return self._grille[lig][col]

	def __setitem__(self, position, valeur):
	    lig, col = position
	    if position in self:
	        self._grille[lig][col] = value

	def objet_dans_case(self, objet_position):
		""" Retourne les coordonnées de la case de l'objet """
		for i in range(0, largeur):
			for j in range(0, longeur):
				if abs(i*self._pas-objet_position[0])<=self._pas and \
				abs(j*self._pas-objet_position[1])<=self._pas:
					return (i, j)
	def case_construction(self, i, j):
		self._liste_cases_construction.append((i, j))
		self._grille[i, j] = 2
	def case_chemin(self, i, j):
		self._liste_cases_chemin.append((i, j))
		self._grille[i, j] = 0 # La case est un chemin

	def case_chemin(self, i, j):
		self._liste_cases_tour.append((i, j))
		self._grille[i, j] = 3 # La case est une tour

	def case_decor(self, i, j):
		self._liste_cases_decor.append((i, j))
class Base:
	def __init__(self, utilisateur, cout_entretien,\
	 cout_amelioration, position, hp = 1):
		self._vie = hp
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._position = position
		self._utilisateur = utilisateur
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
		if self._utilisateur.argent >= self._cout_entretien:
			self._vie += 1
			self._utilisateur.argent -= self._cout_entretien
			self._cout_entretien += 1 # = liste_entretien_base[id_entretien+1] => Creer une liste de couts d'entretiens sur un Excel, pour augmenter le cout d'entretien.

class Tour:
	def __init__(self, position, projectile,hp = 10, portee = 400, cout_construction=10, \
	cout_entretien=2, cout_amelioration = 50, id_tour=0):
		self._projectile = projectile
		self._vie = hp
		self._portee = portee
		self._cout_construction = cout_construction
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._id_tour = id_tour
		self._position = position


class Affichage_fenetre:
	def __init__(self, carte):
		self._liste_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._liste_soldats = ["images/armee/soldat1.png"]
		self._carte = carte



def main():
	pygame.init()

	#Ouverture de la fenêtre Pygame
	fenetre = pygame.display.set_mode((640, 480))
	continuer = 1
	#Chargement et collage du fond
	fond = pygame.image.load("images/interface/background2.jpg").convert()
	fenetre.blit(fond, (0,0))
	pygame.display.flip()
	#Boucle infinie
	while continuer:
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				print event.pos
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer = 0      #On arrête la boucle


if __name__ == '__main__':
    main()
