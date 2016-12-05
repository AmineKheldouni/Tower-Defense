#!/usr/bin/python
#encoding: utf8

#Code pas encore entièrement révisé pour intégration aux autres codes

from armee import*
from objets_interraction import *
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
DT = dt*5

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

class Projectile():
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
    def __init__(self, position_Tour, position_Cible, id_projectile, joueur, soldat_cible):
        self._joueur = joueur
        self._position_initiale = position_Tour
        self._position_initiale = self._joueur.carte.objet_dans_case(self._position_initiale)
        self._position_initiale = self._joueur.carte.positionner_objet((self._position_initiale[0]+0.5, self._position_initiale[1]+1))
        self._position = self._position_initiale
        self._id = id_projectile
        self._soldat_cible = soldat_cible
        self._arrivee = position_Cible
        self._arrivee = self._joueur.carte.objet_dans_case(self._arrivee)
        self._arrivee = self._joueur.carte.positionner_objet((self._arrivee[0]+0.5, self._arrivee[1]+0.5))
        v_x = (position_Cible[0]-position_Tour[0])/5
        v_y = (position_Cible[1]-position_Tour[1])/5
        self._vitesse = (v_x, v_y)
        self._animation = 5. # Nombre d'étapes d'affichage
        self._etape = self._animation #Gere l'animation du projectile
    #
    # def bouge(self):
    #     global dt
    #     '''A appeler à chaque pas de temps dt entre t0 et t0 + DT'''
    #     x=self._position[0]+dt*self._vitesse[0]
    #     y=self._position[1]+dt*self._vitesse[1]
    #     self._position = (x, y)

    # def affichage(self, F):
    #     projectile = pygame.image.load("images/tours/balle.png").convert_alpha()
    #     for k in range(self._animation):
    #         F._fenetre.blit(projectile, self._position)
    #         pas_x, pas_y = (self._arrivee[0]-self._position_initiale[0])/self._animation, \
    #          (self._arrivee[1]-self._position_initiale[1])/self._animation
    #         pos_tmp = self._position_initiale[0]+k*pas_x, \
    #         self._position_initiale[1]+k*pas_y
    #         self._position = pos_tmp
    #         case_projectile = self._joueur._carte.objet_dans_case(self._position)
    def bouge(self):
        pas_x, pas_y = (self._arrivee[0]-self._position_initiale[0])/self._animation, \
        (self._arrivee[1]-self._position_initiale[1]) / self._animation
        pos_tmp = (self._position[0]+pas_x, self._position[1]+pas_y)
        self._position = pos_tmp
        self._etape -= 1

    def set_arrivee(self, pos):
        """ A chaque mouvement du soldat, il faut actualiser la position finale du projectile """
        self._arrivee = pos

    def is_over(self):
        if(self._etape==1):
            #case_projectile = self._joueur.carte.objet_dans_case(self._position)
            #self._soldat_cible.is_dead = True
            return True
        else:
            return False
class Tour(Objet_Interraction):
    def __init__(self, position, joueur, projectile=None, hp = 10, portee = 150, cout_construction=50,
              cout_entretien=2, cout_amelioration = 50, degat = 10, id_tour=1):
        Objet_Interraction.__init__(self,position,0,0)
        #projectile en argument ne sert à rien
        self._cout_construction = cout_construction
        self._id_tour = id_tour
        self._cout_entretien = cout_entretien
        self._vie = hp
        self._portee = portee
        self._degat = degat
        self._joueur = joueur
        self._munitions = 200 # A MODIFIER
        self._cout_amelioration = cout_amelioration
        self._peut_tirer = 0
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

    def attaque(self, armee, F):
        '''_liste_soldat est le tableau des personnages de Armee'''
        '''Renvoie (False/True, un projectile si true)'''
        cible = -1  #indice du soldat de _liste_soldat qui est choisi pour cibles
        distance_cible = 10000000
        for indice_soldat, soldat in enumerate(armee._liste_soldat):
            pos_case = self._joueur._carte.objet_dans_case(soldat._position)
            pos_milieu = pos_case[0]+0.5, pos_case[1]+0.5
            milieu_soldat = self._joueur._carte.positionner_objet(pos_milieu)
            distance_soldat = m.sqrt((milieu_soldat[0]-self._position[0])**2 + (milieu_soldat[1]-self._position[1])**2)
            if distance_soldat < self._portee :
               if distance_soldat < distance_cible:
                   cible = indice_soldat
                   distance_cible = distance_soldat
        if cible != -1 and distance_cible != 10000000 and self._peut_tirer%2 == 0:
            P = Projectile(self._position, armee._liste_soldat[cible]._position, 0, self._joueur, armee._liste_soldat[cible])
            #if self._joueur._carte.objet_dans_case(P._position) != self._joueur._carte.objet_dans_case(P._arrivee): A QUOI SERT CETTE CONDITION ?
            armee._liste_soldat[cible].vie = max(0,armee._liste_soldat[cible].vie-self._degat)
            armee.maj_troupe()
            self._peut_tirer = False
            return (True, P)
        elif (self._peut_tirer%2 != 0):
            self._peut_tirer = True
            return (False,0)
        else:
            return (False,0)


'''
Polymorphisme de tours (pour plus tard)
#class Tour_de_Base(Tour):
#class Tour_d_Elite(Tour):
    #ajouter attribut/capacité : 2 attaques en simultannées
    #changer la portée par exemple'''

"""P=Projectile((0,0),(10,10))
P.bouge()

T=Tour((3,3), P)
T.vieillit()
T.ameliore()
"""
