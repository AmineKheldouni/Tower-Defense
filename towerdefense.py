#!/usr/bin/python
#encoding: utf8
import pygame
from pygame.locals import *

pygame.init()
hauteur = 480
largeur = 630
pas_l = 30
pas_h = 30
nb_cases_h = hauteur/pas_h
nb_cases_l = largeur/pas_l
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((630, 480))

#Chargement et collage du fond
fond = pygame.image.load("images/interface/background2.jpg").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso = pygame.image.load("images/tours/tour2.png").convert_alpha()
fenetre.blit(perso, (200,300))



route = pygame.image.load("images/interface/route.jpg").convert_alpha()
for i in range(0, nb_cases_l):
	fenetre.blit(route, (i*largeur/nb_cases_l, hauteur/nb_cases_h*(nb_cases_h//2)))


base = pygame.image.load("images/interface/arbre.png").convert_alpha()
fenetre.blit(base, ((nb_cases_l-1)*largeur/nb_cases_l, hauteur/nb_cases_h*(nb_cases_h//2)))

#Chargement place de construction
place_construction = pygame.image.load("images/tours/tour1.png").convert_alpha()
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
		if event.type == QUIT:     #Si un de ces événements est de type QUIT
			continuer = 0      #On arrête la boucle
