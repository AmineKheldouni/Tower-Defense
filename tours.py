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

dt = 1
DT = dt*5

class Projectile(object):
    """ Seules les méthodes dégâts et etats sont à modifier lors de la création d'un nouveau Projectile"""
    def __init__(self, position_Tour, position_Cible, id_projectile, C, soldat_cible,degat):
        self._animation = 5
        position_initiale = position_Tour
        pos_init_case = C.objet_dans_case(position_initiale)
        position_initiale = C.positionner_objet((pos_init_case[0]+0.5, pos_init_case[1]+1))
        self._position = position_initiale
        self._id = id_projectile
        self._soldat_cible = soldat_cible
        arrivee = position_Cible
        arrivee_case = C.objet_dans_case(arrivee)
        arrivee = C.positionner_objet((arrivee_case[0]+0.5, arrivee_case[1]+0.5))
        self.v_x = (arrivee[0]-self._position[0])/self._animation
        self.v_y = (arrivee[1]-self._position[1])/self._animation
         # Nombre d'étapes d'affichage
        self._etape = self._animation #Gere l'animation du projectile
        self._degat = degat

    def bouge(self,C):
        pos_tmp = (self._position[0]+self.v_x, self._position[1]+self.v_y)
        arrivee = C.positionner_objet((self._soldat_cible._position[0]+0.5, self._soldat_cible._position[1]+0.5))
        self.v_x = (arrivee[0]-self._position[0])/self._animation
        self.v_y = (arrivee[1]-self._position[1])/self._animation
        self._position = pos_tmp
        self._etape -= 1
        if(self.is_over()):
            self.degat_projectile()
            self.effet_projectile()


    # def set_arrivee(self, pos):
    #     """ A chaque mouvement du soldat, il faut actualiser la position finale du projectile """
    #     self._arrivee = pos

    def degat_projectile(self):
        self._soldat_cible.dommage(self._degat)

    def effet_projectile(self):
        return 0

    def is_over(self):
        if(self._etape==0):
            return True
        else:
            return False

class Projectile_Glace(Projectile):
    """Utilisée par les tours de glace"""
    def __init__(self, position_Tour, position_Cible, id_projectile, C, soldat_cible,degat):
        super(Projectile_Glace, self).__init__(position_Tour, position_Cible, id_projectile, C, soldat_cible,degat)
    def effet_projectile(self):
        self._soldat_cible.change_etat(Glace())

class Projectile_Feu(Projectile):
    """Utilisée par les tours de glace"""
    def __init__(self, position_Tour, position_Cible, id_projectile, C, soldat_cible,degat):
        super(Projectile_Feu, self).__init__(position_Tour, position_Cible, id_projectile, C, soldat_cible,degat)
    def effet_projectile(self):
        self._soldat_cible.change_etat(Feu())

'''
Seuls les fonctions choisir cibles et l'attributs projectiles sont à changer pour les classes filles (ainsi que l'id
'''

class Tour(Case):
    def __init__(self, position, id_tour):
        self._id_tour = id_tour
        self._cout_construction = ExtractIntFromFile("data_tourelle.csv",id_tour+1,3)
        self._cout_entretien    = ExtractIntFromFile("data_tourelle.csv",id_tour+1,4)
        self._cout_amelioration = ExtractIntFromFile("data_tourelle.csv",id_tour+1,5)
        self._portee            = ExtractIntFromFile("data_tourelle.csv",id_tour+1,6)
        self._degat             = ExtractIntFromFile("data_tourelle.csv",id_tour+1,7)
        self._vitesse           = ExtractIntFromFile("data_tourelle.csv",id_tour+1,8)
        self.vie_initiale       = ExtractIntFromFile("data_tourelle.csv",id_tour+1,9)
        self._munitions_max     = ExtractIntFromFile("data_tourelle.csv",id_tour+1,10)
        self._id_excel          = ExtractIntFromFile("data_tourelle.csv",id_tour+1,11)

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
        self._vie += self._vie/2
        self._portee += 1
        self._degat += self.degat/10
        self._cout_amelioration += self._cout_amelioration/2
        self._cout_entretien += 20
        self._munitions_max += self._munitions_max/5

    def repare(self):
        self._munitions = self.munitions_max
        self._id_graphic = self._id_tour+50

    def peut_tirer(self):
        return self._munitions>0 and self._chargement>100

    def projectile(self,soldat,carte):
        return Projectile(self._position, carte.positionner_objet(soldat._position), 0, carte, soldat, self._degat)

    # def est_a_porte(self, pos):
    #     print(self._position)
    #     return  abs(self._position[0] - pos[0]) <= self._portee and abs(self._position[1]-pos[1]) <= self._portee

    def attaque(self, armee, C):
        '''_liste_soldat est le tableau des personnages de Armee'''
        '''Renvoie (False/True, un projectile si true)'''
        cible = -1  #indice du soldat de _liste_soldat qui est choisi pour cibles
        distance_cible = 10000000
        for indice_soldat, soldat in enumerate(armee._liste_soldat):
            pos_case = soldat._position
            pos_tour = C.objet_dans_case(self.position)
            # distance_soldat = abs(pos_tour[0]-pos_case[0])+abs(pos_tour[1]-pos_case[1])
            distance_soldat = max(abs(pos_tour[0]-pos_case[0]), abs(pos_tour[1]-pos_case[1]))
            if  distance_soldat <= self._portee  :
               if distance_soldat < distance_cible:
                   cible = indice_soldat
                   distance_cible = distance_soldat
        if cible != -1 and self.peut_tirer():
            self._chargement-=100
            P = self.projectile(armee._liste_soldat[cible],C)
            self._munitions -= 1
            return (True, P)
        else:
            return (False,0)

    def actualisation(self):
        self._chargement+=self._vitesse
        if(self._munitions<=0):
            self._id_graphic=53

class Tour_Feu(Tour):
    def __init__(self, position, id_tour):
        super(Tour_Feu, self).__init__(position, id_tour)
    def projectile(self,soldat,carte):
        return Projectile_Feu(self._position, carte.positionner_objet(soldat._position), 0, carte, soldat, self._degat)

class Tour_Glace(Tour):
    def __init__(self, position, id_tour):
        super(Tour_Glace, self).__init__(position, id_tour)
    def projectile(self,soldat,carte):
        return Projectile_Glace(self._position, carte.positionner_objet(soldat._position), 0, carte, soldat, self._degat)
