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

dt = 1
DT = dt*5

class Projectile():
    def __init__(self, position_Tour, position_Cible, id_projectile, C, soldat_cible,degat):
        self._animation = 5
        position_initiale = position_Tour
        position_initiale = C.objet_dans_case(position_initiale)
        position_initiale = C.positionner_objet((position_initiale[0]+0.5, position_initiale[1]+1))
        self._position = position_initiale
        self._id = id_projectile
        self._soldat_cible = soldat_cible
        arrivee = position_Cible
        arrivee = C.objet_dans_case(arrivee)
        arrivee = C.positionner_objet((arrivee[0]+0.5, arrivee[1]+0.5))
        self.v_x = (arrivee[0]-self._position[0])/self._animation
        self.v_y = (arrivee[1]-self._position[1])/self._animation
         # Nombre d'étapes d'affichage
        self._etape = self._animation #Gere l'animation du projectile
        self._degat = degat

    def bouge(self):
        pos_tmp = (self._position[0]+self.v_x, self._position[1]+self.v_y)
        self._position = pos_tmp
        self._etape -= 1

    def set_arrivee(self, pos):
        """ A chaque mouvement du soldat, il faut actualiser la position finale du projectile """
        self._arrivee = pos

    def is_over(self):
        if(self._etape==0):
            self._soldat_cible._vie= max(0,self._soldat_cible._vie-self._degat)
            return True
        else:
            return False

'''
Seuls les fonctions choisir cibles et l'attributs projectiles sont à changer pour les classes filles (ainsi que l'id)
'''

class Tour(Case):
    def __init__(self, position, id_tour):
        self._id_tour = id_tour
        self._cout_construction = extract("tourelle",id_tour+1,3)
        self._cout_entretien    = extract("tourelle",id_tour+1,4)
        self._cout_amelioration = extract("tourelle",id_tour+1,5)
        self._portee            = extract("tourelle",id_tour+1,6)
        self._degat             = extract("tourelle",id_tour+1,7)
        self._vitesse           = extract("tourelle",id_tour+1,8)
        self.vie_initiale       = extract("tourelle",id_tour+1,9)
        self._munitions_max     = extract("tourelle",id_tour+1,10)
        self._id_excel          = extract("tourelle",id_tour+1,11)

        self._vie = self.vie_initiale
        self._munitions = self._munitions_max
        self._chargement = 0
        super(Tour,self).__init__(position, "tour", 0,self._id_excel,0)
        #du prochain niveau de tour, pour passer id_tour=2

	# A COMPLETER
    @property
    def position(self):
        return self._position
    @property
    def degat(self):
        return self._degat
    @property
    def cout_amelioration(self):
        return self._cout_amelioration
    @property
    def munitions_max(self):
        return self._munitions_max
    @property
    def cout_entretien(self):
        return self._cout_entretien

    @property
    def munitions(self):
        return self._munitions

    @property
    def portee(self):
        return self._portee

    def vieillit(self):
        #à appeler si le joueur n'a plus d'argent pour l'entretenir
        self._vie -= 2*self.vie//9

    def ameliore(self, C):
        # A MODIFIER ET ADAPTER PAR RAPPORT A LEXCEL
        print("Ameliration de la tour")
        self._vie += 100
        self._portee += C.nb_cases_h
        self._degat *= 4
        self._cout_amelioration *= 2
        self._cout_entretien *= 2
        self._munitions_max *= 2
    def repare(self):
        print("Reparation de la tour")
        self._munitions = self.munitions_max
        self._id_graphic = self._id_tour+50

    def peut_tirer(self):
        return self._munitions>0 and self._chargement>100

    def choisir_cible(self,soldat_1,soldat_2):

        return

    def attaque(self, armee, F, C):
        '''_liste_soldat est le tableau des personnages de Armee'''
        '''Renvoie (False/True, un projectile si true)'''
        cible = -1  #indice du soldat de _liste_soldat qui est choisi pour cibles
        distance_cible = 10000000
        for indice_soldat, soldat in enumerate(armee._liste_soldat):
            pos_case = soldat._position
            pos_tour = C.objet_dans_case(self.position)
            distance_soldat = abs(pos_tour[0]-pos_case[0])+abs(pos_tour[1]-pos_case[1])
            if distance_soldat < self._portee/C.nb_cases_l :
               if distance_soldat < distance_cible:
                   cible = indice_soldat
                   distance_cible = distance_soldat
        if cible != -1 and self.peut_tirer():
            self._chargement-=100;
            P = Projectile(self._position, C.positionner_objet(armee._liste_soldat[cible]._position), 0, C, armee._liste_soldat[cible], self._degat)
            self._munitions -= 1
            return (True, P)
        else:
            return (False,0)

    def actualisation(self):
        self._chargement+=self._vitesse
        if(self._munitions<=0):
            self._id_graphic=53

def TourFeu(Tour):
    def __init(self):
        super(TourFeu, self).__init__()
        self.id_excel = 51
        Tour._portee = 100

def TourGlace(Tour):
    def __init(self):
        super(TourGlace, self).__init__()
        self.id_excel = 52
        Tour._portee = 200
