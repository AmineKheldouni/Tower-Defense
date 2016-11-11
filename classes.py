#!/usr/bin/python
#encoding: utf8
import pygame
from pygame.locals import *

class Carte:
	def __init__(hauteur, largeur):
		self._hauteur = hauteur
		self._largeur = largeur
		self._grille = [[1 for i in range(largeur)] for j in range(hauteur)]
		self._carte_couts = [10000]

	def __getitem__(self, position):
