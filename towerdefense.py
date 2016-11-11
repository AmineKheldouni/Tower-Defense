#!/usr/bin/python
#encoding: utf8
import pygame
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((640, 480))

#Chargement et collage du fond
fond = pygame.image.load("images/background2.jpg").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso = pygame.image.load("images/tower.png").convert_alpha()
fenetre.blit(perso, (200,300))



#Chargement place de construction
place_construction = pygame.image.load("images/tourelle2.png").convert_alpha()
pos_place_construction = place_construction.get_rect()
fenetre.blit(place_construction, pos_place_construction)


#Rafraîchissement de l'écran
pygame.display.flip()

continuer = 1

#Boucle infinie
while continuer:
	for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			pos_mouse = event.pos
			print pos_mouse
			pos_place_construction.move(pos_mouse[0], pos_mouse[1])
		if event.type == QUIT:     #Si un de ces événements est de type QUIT
			continuer = 0      #On arrête la boucle
