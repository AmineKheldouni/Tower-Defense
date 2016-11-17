#!/usr/bin/python
#encoding: utf8

#Code pas encore entièrement révisé pour intégration aux autres codes

from armee import*

import pygame
from pygame.locals import *

import functools
from functools import partial
import copy
import sys
import numpy as np

import math


'''Il y a 2 échelles de temps : dt = entre deux affichages du jeu
et DT = N*dt (ou N à fixer) entre deux affichages du jeu où le joueur peut agir
Mieux si variables globales.'''

dt = 1
DT = 5

'''
Pour Yo :
1/ DANS L'AFFICHAGE APPELER bouge(PROJECTILE) tous les dt entre 0 et DT
et ne laisser au joueur l'opportunité de jouer qu'aux multiples de DT
pour toutes les tours. Attention si le projectile n'existe pas !!!
2/ AJOUTER LA FONCTIONNALITE AMELIORER et associer le signal à AMELIORE
3/ APPELER "viellit" aux multiples de DT si le joueur ne peut payer l'entretien

du type :
    t=0
    affiche(jeu)
    while notEndgame (armee eliminee ou base detruite) :
        t+=dt
        if t%DT = 0 :
            on donne la possibilité au joueur de construire/améliorer
            et AFFICHER JEU à chaque opération puis ATTENDRE

         sinon il fait que regarder pendant dt :
            attaque(tour)
            bouge(projectile) pour toutes les tours où projectile existe
            vieillit(tour) si peut plus payer
            AFFICHER LE JEU pendant dt
'''

class Projectile:
    '''
    Yo considère le mouvement de Projectile pour un jeu tout par tour (ie le
    joueur ne fait rien pendant DT et regarde le projectile atteindre sa cible)
    (dt est le temps entre deux affichages du jeu où on donne la possibilité
    au joueur d'agir ; il y a des affichages du jeu pendant dt mais le joueur ne peut
    rien faire)
    Il y a donc deux échelles de temps : dt = entre deux affichages du jeu
    et DT = N*dt (ou N à fixer) entre deux affichages du jeu où le joueur peut jouer
    Mieux si variables globales.
    '''

    def __init__(self, position_Tour, position_Cible):
        global DT
        self._position = position_Tour
        v_x = (position_Cible[0]-position_Tour[0])//DT
        v_y = (position_Cible[1]-position_Tour[1])//DT
        self._vitesse = (v_x,v_y)

    def bouge(self):
        global dt
        '''A appeler à chaque pas de temps dt entre t0 et t0 + DT'''
        x=self._position[0]+dt*self._vitesse[0]
        y=self._position[1]+dt*self._vitesse[1]
        self._position = (x,y)

class Tour:
    def __init__(self, position, joueur, projectile=None, hp = 10, portee = 400, cout_construction=10,
              cout_entretien=2, cout_amelioration = 50, degat = 10, id_tour=1):

        #projectile en argument ne sert à rien
        self._cout_construction = cout_construction

        self._id_tour = id_tour
        self._position = position
        self._cout_entretien = cout_entretien
        self._projectile = None
        self._vie = hp
        self._portee = portee
        self._degat = degat
        self._joueur = joueur
        self._cout_amelioration = cout_amelioration
        #du prochain niveau de tour, pour passer id_tour=2

	# A COMPLETER

    def vieillit(self):
        #à appeler si le joueur n'a plus d'argent pour l'entretenir
        self._portee /= 2

    def ameliore(self):
        #à appeler si le joueur demande une amélioration et a l'argent nécessaire
        #pour le faire
        #Les améliorations peuvent porter sur 3 choses : VIE/PORTEE/DEGAT
        #paramètres d'amélioration à modifier peut-être avec une IA
        self._id_tour += 1

        self._vie *= 2
        self._portee *= 2
        self._degat *= 2

        self._cout_amelioration *= 2

    def attaque(self,armee):
        '''_liste_soldat est le tableau des personnages de Armee'''
        cible = -1  #indice du soldat de _liste_soldat qui est choisi pour cibles
        distance_cible = 10000000
        for indice_soldat, soldat in enumerate(armee._liste_soldat):
            distance_soldat = m.sqrt((soldat._position[0]-self._position[0])**2 + (soldat._position[1]-self._position[1])**2)
            if distance_soldat < self._portee :
               if distance_soldat < distance_cible:
                   cible = indice_soldat
                   distance_cible = distance_soldat

        if cible != -1 :
            self._projectile = Projectile(self._position, soldat._position)
            armee._liste_soldat[cible].vie = max(0,armee._liste_soldat[cible].vie-self._degat)

'''
Polymorphisme de tours (pour plus tard)
#class Tour_de_Base(Tour):
#class Tour_d_Elite(Tour):
    #ajouter attribut/capacité : 2 attaques en simultannées
    #changer la portée par exemple'''

'''class Tour:
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
  # A COMPLETER'''

P=Projectile((0,0),(10,10))
P.bouge()

T=Tour((3,3), P)
T.vieillit()
T.ameliore()
