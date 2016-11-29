#!/usr/bin/python
#encoding: utf8

import pygame
from pygame.locals import *

from gestion_fenetre import *
from tours import *

import functools
from functools import partial
import copy
import sys
import numpy as np
import math as m
import copy
import numpy.random as rd
import time

#ATTENTION CE QUI SUIT EST DU PSEUDO-CODE
#Les fonctions de l'affichage du menu doivent être dans Menu !!! et non dans Affichage

class Menu():
    def __init__(self, joueur):
        self._hauteur = 150
        self._largeur = 1250
        self._nb_cases_h = 3
        self._nb_cases_l = 25
        self._type_objet = None
        self._joueur = joueur
        self._dict_infos=None
        self._dict_boutons=None

    def menu_statique(self):
        """ Affiche l'argent et le score du joueur """
        
    def menu_tour(self, event, F):
        """ Affiche l'image, les caractéristiques (vie, dégat) et les boutons"""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self.carte.objet_dans_case(event.pos)
            if self.carte[pos_x, pos_y] == "Tour":
                self._type_objet="Tour"
                for i in range(len(self._joueur.liste_tours)):
                    case_tour = self._joueur.carte.objet_dans_case(\
                                        self._joueur.liste_tours[i].position)
                    if (case_tour==(pos_x, pos_y)):
                        T = self._joueur.liste_tours[i]
                        pos_image = (500, self._joueur.carte.hauteur+self._hauteur/2) # image
                        pos_vie=  (600, self._joueur.carte.hauteur+150/6)            #attributs
                        pos_degat= (600, self._joueur.carte.hauteur+150/6*2)
                        pos_portee= (600, self._joueur.carte.hauteur+150/6*3)
                        pos_cout_amelioration= (600, self._joueur.carte.hauteur+150/6*4)
                        pos_cout_entretien= (600, self._joueur.carte.hauteur+150/6*5)
                        pos_bouton_ameliorer=(800, self._joueur.carte.hauteur+150/3)
                        pos_bouton_entretenir=(800, self._joueur.carte.hauteur+150/3*2)       # boutton
                        self._dict_infos = {
                                        "vie : ":pos_vie,
                                        "dégats : ":pos_degat,
                                        "portée : ":pos_portee,
                                        "couts d'amélioration : ":pos_cout_amelioration,
                                        "couts d'entretien : ":pos_cout_entretien}
                        self._dict_boutons = {"/images/interface/ameliorer.png":pos_bouton_ameliorer,
                                           "/images/interface/entretenir.png":pos_bouton_entretenir
                                           }

                        image_tour = pygame.image.load("images/tours/tour"+str(T._id_tour)+".png").convert_alpha()
                        F.blit(image_tour, pos_image)

                        for d in dict_infos.keys():
                            font_donnee = pygame.font.Font(None, 20)
                    	    text_donnee = font_donnee.render(d, 1, (255, 255, 255))
                            self._fenetre.blit(text_donnee, dict_infos[d])
                        for b in dict_boutons.keys():
                            image_ameliorer = pygame.image.load(b).convert_alpha()
                            F.blit(b, dict_boutons[b])

        if event.type == MOUSEBUTTONDOWN and event.button == 1 and type_objet=="Tour":
            pos_x, pos_y = event.pos
            for key in self._dict_boutons.keys():
                pos = (pos_x,pos_y)
                if self._dict_boutons[key]==pos:
                    T.ameliorer()

    def objet_dans_case(self, objet_position):
        """ Retourne les coordonnées de la case de l'objet """
        pas_l = int(self.largeur/self.nb_cases_l)
        pas_h = int(self.hauteur/self.nb_cases_h)
        return (objet_position[0]//pas_l, objet_position[1]//pas_h)

    def positionner_objet(self, pos_case):
        a = int(pos_case[0]*self.largeur/self.nb_cases_l)
        b = int(pos_case[1]*self.hauteur/self.nb_cases_h)
        return (a, b)
"""
    def interaction_tour():
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self.carte.objet_dans_case(event.pos)
            self._menu=enu("Tour",_liste_tours[i] tq _liste_tours[i].pos=pos_x, pos_y, pos_x,posy)
			# PROPOSER AMELIORATION OU REPARATION
            print ("Amélioration ? Réparation ?")
		elif self.carte[pos_x, pos_y] == "place construction":
    		pos_pix = pos_x*self.carte._largeur/self.carte._nb_cases_l\
    		, pos_y*self.carte._hauteur/self.carte._nb_cases_h
                self._menu=Menu("place construction", None)
           else self.carte[pos_x, pos_y] == "base":
               #OU STOCKE T'ON BASE ?
               self._menu=Menu("base", liste_base[i] tq _liste_bases[i].pos=pos_x, pos_y)


          if self._type_objet="place construction":
              #selon le type de l'objet on construit la grille d'affichage
              #sous la forme (photo, liste des infos à savoir, options cliquables
              #par le joueur

              self._affichage[2][0] = 0"images/interface/background2.jpg",None,bouton construire avec les infos dessus (accesible depuis fichier...)]
              self._nb_cases_h = 1
	      	self._nb_cases_l = 2
              positionner_objet(self._affichage)
              affiche(self._affichage)
              sous_menu(place,pos_x,pos_y)
              affiche(self._affichage)
          if type_objet()="tour":
              #selon le type de l'objet on construit la grille d'affichage
              #sous la forme (photo, liste des infos à savoir, options cliquables
              #par le joueur)
              self._affichage = [image,[attributs de tour],[bouton ameliorer,bouton reparer]]
              positionner_objet(self._affichage)
              affiche(self._affichage)
              sous_menu(tour)
              affiche(self._affichage)
          if type_objet()="place base":
              #selon le type de l'objet on construit la grille d'affichage
              #sous la forme (photo, liste des infos à savoir, options cliquables
              #par le joueur)
              self._affichage = [image,[les infos de la base],bouton_fermer]
              positionner_objet(self._affichage)
              affiche(self._affichage)
              sous_menu(base)
              affiche(self._affichage)

     def sous_menu_tour(self, event):
         self.
         if clique_sur_bouton(reparation): #recupere pos avec objet dans case propre à menu
              reparer(_liste_tours[i])
              self._menu = None
          if clique_sur_bouton(amelioration): #avec objet dans case propre à menu
              ameliorer(_liste_tours[i])
              self._menu = None

      def sous_menu_place(self, event,pos_x,pos_y):
		if clique_sur_bouton(construire): #avec objet dans case propre à menu
                    T = Tour(pos_pix, self)
				if T._cout_construction <= self._argent:
					self._liste_tours.append(T)
					self._argent -= T._cout_construction
					self._carte[pos_x, pos_y] = "tour"
					if pos_y>0:
						self._carte[pos_x, pos_y-1] = "tour"
				else:
					print ("Vous n'avez pas suffisamment d'argent.")
                    self.menu=None
     def sous_menu_base(self.event):
         if clique_sur_bouton(fermer): #avec objet dans case propre à menu
              self._menu=None

	@property
	def largeur(self):
		return self._largeur
	@property
	def hauteur(self):
		return self._hauteur
	@property
	def nb_cases_h(self):
		return self._nb_cases_h
	@property
	def nb_cases_l(self):
		return self._nb_cases_l
	def __contains__(self, position):
	    lig, col = position
	    return (lig >= 0) and (lig < self._nb_cases_l) and (col >= 0) \
		and (col < self._nb_cases_h)
	def __getitem__(self, position):
		lig, col = position
		if position in self:
			return self._passeport[lig][col]
	def __setitem__(self, position, valeur):
	    lig, col = position
	    if position in self:
	        self._passeport[lig][col] = valeur
"""
