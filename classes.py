#!/usr/bin/python
#encoding: utf8
import pygame
from pygame.locals import *

class Carte:
	def __init__(self, hauteur, largeur, pas):
		self._hauteur = hauteur
		self._largeur = largeur
		self._pas = pas
		self._grille = [[1 for i in range(largeur)] for j in range(hauteur)]
		self._carte_couts = [10000]
@property
	def carte_couts(self):
		return self._carte_couts
    def __contains__(self, position):
        lig, col = position
        return (lig >= 0) and (lig < self._largeur) \
           and (col >= 0) and (col < self._hauteur)
	def __getitem__(self, position):
		lig, col = position
		if position in self:
			return self._grille[lig][col]
	def __setitem__(self, position, valeur):
        lig, col = position
        if position in self:
            self._grille[lig][col] = value


class Base:
	def __init__(self, hp = 1, utilisateur, cout_entretien,\
	 cout_amelioration, position):
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
class Affichage_fenetre:
	def __init__(self, carte):
		self._liste_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._liste_soldats = ["images/armee/soldat1.png"]
		self._carte = carte
