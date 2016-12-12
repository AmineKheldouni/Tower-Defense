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

#Les fonctions de l'affichage du menu doivent être dans Menu !!! et non dans Affichage

class Menu():
    def __init__(self, joueur):
        self._joueur = joueur
        self._hauteur = 150
        self._largeur = self._joueur.carte.largeur
        self._nb_cases_h = 3
        self._nb_cases_l = 25
        self._type_objet = None
        self._index_objet = None #reperer l'objetdans les attributs de joueur
        self._dict_infos=None
        self._dict_boutons=None

    @property
    def carte(self):
        return self._joueur.carte
    def affichage_menu_haut(self, F):
        """ Menu du haut de fenetre : Temps, Vie des bases, argent du joueur et son score """
        # Affichage du temps (Min:Sec)
        font_temps = pygame.font.Font(None, 36)
        temps = pygame.time.get_ticks()
        temps /= 1000
        secondes = temps%60
        minutes = temps//60
        text_temps = font_temps.render(str(minutes)+ " : "+ str(secondes), 1, (255, 255, 255))
        F.blit(text_temps, (20,10))
        # Affichage des vies des bases
        pos_vie = []
        for i in range(len(self._bases)):
                pos_vie.append(self.carte.positionner_objet((self.carte.nb_cases_l-len(self._bases)+i, 0)))
        for i, b in enumerate(self._bases):
        	if b._vie > b.vie_depart/2:
                       self.ajouter_element("images/interface/bases/hp_base.png", pos_vie[i])
        	elif b._vie > b.vie_depart/5 and b._vie <= b.vie_depart/2:
                       self.ajouter_element("images/interface/bases/hp_base2.png", pos_vie[i])
        	else:
                       self.ajouter_element("images/interface/bases/hp_base3.png", pos_vie[i])

    def menu_statique(self, F):
        """ Affiche l'argent et le score du joueur """
        # Argent :
        pos_image = (0, self._joueur.carte.hauteur+self._hauteur//5)
        image_or = pygame.image.load("images/interface/or1.png").convert_alpha()
        F._fenetre.blit(image_or, pos_image)
        font_or = pygame.font.Font(None, 50)
        or_joueur = str(self._joueur.argent)
        texte_or = font_or.render(or_joueur, 1, (255, 255, 0))
        F._fenetre.blit(texte_or, (60, pos_image[1]+5))

        # Score :
        pos_image = (0, self._joueur.carte.hauteur+3*self._hauteur//5)
        image_score = pygame.image.load("images/interface/etoile.png").convert_alpha()
        F._fenetre.blit(image_score, pos_image)
        font_score = pygame.font.Font(None, 50)
        score_joueur = str(self._joueur.score)
        texte_score = font_score.render(score_joueur, 1, (0, 0, 255))
        F._fenetre.blit(texte_score, (60, pos_image[1]+5))

    def affichage_menu_haut(self, Affichage):
    	""" Menu du haut de fenetre : Temps, Vie des bases, argent du joueur et son score """
    	# Affichage du temps (Min:Sec)
    	font_temps = pygame.font.Font(None, 36)
    	temps = pygame.time.get_ticks()
    	temps /= 1000
    	secondes = temps%60
    	minutes = temps//60
    	text_temps = font_temps.render(str(minutes)+ " : "+ str(secondes), 1, (255, 255, 255))
    	Affichage._fenetre.blit(text_temps, (20,10))
    	# Affichage des vies des bases
    	pos_vie = []
    	for i in range(len(Affichage._bases)):
    		pos_vie.append(Affichage.carte.positionner_objet((Affichage.carte.nb_cases_l-len(Affichage._bases)+i, 0)))

    	for i, b in enumerate(Affichage._bases):
    		if b._vie > b.vie_depart/2:
    			Affichage.ajouter_element("images/interface/bases/hp_base.png", pos_vie[i])
    		elif b._vie > b.vie_depart/5 and b._vie <= b.vie_depart/2:
    			Affichage.ajouter_element("images/interface/bases/hp_base2.png", pos_vie[i])
    		else:
    			Affichage.ajouter_element("images/interface/bases/hp_base3.png", pos_vie[i])
    def maj_menu(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self._joueur.carte.objet_dans_case(event.pos)
            if self.carte.cases[pos_x][pos_y].type_objet == 5:
                self._type_objet = 5
            if self.carte.cases[pos_x][pos_y].type_objet == 102:
                self._type_objet = 102

    def menu_tour(self, event, F):
        """ Affiche l'image, les caracteristiques (vie, degat) et les boutons"""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self._joueur.carte.objet_dans_case(event.pos)
            if self.carte.cases[pos_x][pos_y].type_objet == 5:
                self._type_objet= 5
                pos_image = (1*self.carte.largeur/7, self._joueur.carte.hauteur+self._hauteur/3) # image
                pos_vie=  (3*self.carte.largeur/7, self._joueur.carte.hauteur+150/6)            #attributs
                pos_degat= (3*self.carte.largeur/7, self._joueur.carte.hauteur+150/6*2)
                pos_portee= (3*self.carte.largeur/7, self._joueur.carte.hauteur+150/6*3)
                pos_cout_amelioration= (3*self.carte.largeur/7, self._joueur.carte.hauteur+150/6*4)
                pos_cout_entretien= (3*self.carte.largeur/7, self._joueur.carte.hauteur+150/6*5)
                pos_bouton_ameliorer=(5*self.carte.largeur/7, self._joueur.carte.hauteur+150/3)
                pos_bouton_entretenir=(5*self.carte.largeur/7, self._joueur.carte.hauteur+150/3*2)       # boutton
                for i in range(len(self._joueur.liste_tours)):
                    self._index_objet = i
                    tour=self._joueur.liste_tours[i]
                    case_tour = self._joueur.carte.objet_dans_case(\
                                        tour.position)
                    if (case_tour==(pos_x, pos_y)):
                        self._dict_infos = {
                                        "vie : ":(pos_vie,tour._vie),
                                        "degats : ":(pos_degat,tour._degat),
                                        "portee : ":(pos_portee,tour._portee),
                                        "couts d'amelioration : ":(pos_cout_amelioration,tour._cout_amelioration),
                                        "couts d'entretien : ":(pos_cout_entretien,tour._cout_entretien)}
                        self._dict_boutons = {"ameliorer":("images/interface/amelioration.png",pos_bouton_ameliorer),
                                           "entretenir":("images/interface/reparation.png",pos_bouton_entretenir)
                                           }
                        image_tour = pygame.image.load("images/tours/tour"+".png").convert_alpha()
                        F.blit(image_tour, pos_image)
                        for d in self._dict_infos.keys():
                            font_donnee = pygame.font.Font(None, 20)
                    	    text_donnee = font_donnee.render(d+" "+str(self._dict_infos[d][1]), 1, (255, 255, 255))
                            F.blit(text_donnee, self._dict_infos[d][0])
                        for b in self._dict_boutons.keys():
                            image = pygame.image.load(self._dict_boutons[b][0]).convert_alpha()
                            F.blit(image, self._dict_boutons[b][1])

            if (((event.type == MOUSEBUTTONDOWN) and (event.button == 1)) and (self._type_objet==5)):
                pos_x, pos_y = self.carte.objet_dans_case(event.pos)
                pos = (pos_x,pos_y)
                for b in self._dict_boutons.keys():
                    if ((pos[0]>=self._dict_boutons[b][1][0])and(pos[0]<=self._dict_boutons[b][1][0]+50)):
                        if ((pos[1]>=self._dict_boutons[b][1][1])and(pos[1]<=self._dict_boutons[b][1][1]+50)):
                            if (self._dict_boutons[b][0]=="ameliorer"):
                                objet=self._joueur.liste_tours[self._index_objet]
                                if objet._cout_amelioration<=self._joueur._argent:
                                    self._argent -= objet._cout_amelioration
                                    self._joueur.liste_tours[self._index_objet].ameliore()
                            """else :
                                F.blit("Argent non suffisant",self._dict_boutons[b][1][0])
                            if (self._dict_boutons[b][0]=="entretenir"):
                               objet=self._joueur.liste_tours[self._index_objet]
                                if objet._cout_entretien<=self._joueur._argent:
                                    self._argent -= objet._cout_entretien
                                    self._joueur.liste_tours[self._index_objet].entretient()  #creer une telle methode (score, points de vie...)
                                else :
                                    F.blit("Argent non suffisant",self._dict_boutons[b][1][0])"""

    def menu_place_construction(self, event, F):
        """ Affiche l'image, les caracteristiques (vie, degat) et les boutons"""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self.carte.objet_dans_case(event.pos)
            if self.carte.cases[pos_x][pos_y].type_objet == 102:
                self._type_objet="place"
                pos_image = (2*self.carte.largeur/6, self._joueur.carte.hauteur+self._hauteur/2) # image
                pos_vie=  (3*self.carte.largeur/6, self._joueur.carte.hauteur+150/6)            #attributs
                pos_degat= (3*self.carte.largeur/6, self._joueur.carte.hauteur+150/6*2)
                pos_portee= (3*self.carte.largeur/6, self._joueur.carte.hauteur+150/6*3)
                pos_cout_amelioration= (3*self.carte.largeur/6, self._joueur.carte.hauteur+150/6*4)
                pos_cout_entretien= (3*self.carte.largeur/6, self._joueur.carte.hauteur+150/6*5)
                pos_bouton_ameliorer=(5*self.carte.largeur/6, self._joueur.carte.hauteur+150/3)
                pos_bouton_entretenir=(5*self.carte.largeur/6, self._joueur.carte.hauteur+150/3*2)       # boutton
                #Creer une tout virtuelle pour avoir les infos avant
                self._dict_infos = {
                                "vie : ":(pos_vie,tour._vie),
                                "degats : ":(pos_degat,tour._degat),
                                "portee : ":(pos_portee,tour._portee),
                                "couts d'amelioration : ":(pos_cout_amelioration,tour._cout_amelioration),
                                "couts d'entretien : ":(pos_cout_entretien,tour._cout_entretien)}
                self._dict_boutons = {"construire":("/images/interface/ameliorer.png",pos_bouton_ameliorer)}

                image_tour = pygame.image.load("images/tours/tour"+str(T._id_tour)+".png").convert_alpha()
                F.blit(image_tour, pos_image)

                for d in self._dict_infos.keys():
                    font_donnee = pygame.font.Font(None, 20)
            	    text_donnee = font_donnee.render(d, 1, (255, 255, 255))
                    F.blit(text_donnee, self._dict_infos[d])
                for b in self._dict_boutons.keys():
                    image = pygame.image.load(self._dict_boutons[b][0]).convert_alpha()
                    F.blit(self._dict_boutons[b][0], self._dict_boutons[b][1])

        if event.type == MOUSEBUTTONDOWN and event.button == 1 and type_objet==5:
            pos_x, pos_y = self.carte.objet_dans_case(event.pos)
            pos = (pos_x,pos_y)
            for b in self._dict_boutons.keys():
                if ((pos[0]>=self._dict_boutons[b][1][0])and(pos[0]<=self._dict_boutons[b][1][0]+2000)):
                    if ((pos[1]>=self._dict_boutons[b][1][1])and(pos[1]<=self._dict_boutons[b][1][1]+150/3)):
                        if (self._dict_boutons[b][0]=="ameliorer"):
                            objet=self._joueur.liste_tours[self._index_objet]
                            if objet._cout_amelioration<=self._joueur._argent:
                                self._argent -= objet._cout_amelioration
                                self._joueur.liste_tours[self._index_objet].ameliore()
                            else :
                                F.blit("Argent non suffisant",self._dict_boutons[b][1][0])
                        if (self._dict_boutons[b][0]=="entretenir"):
                            objet=self._joueur.liste_tours[self._index_objet]
                            if objet._cout_entretien<=self._joueur._argent:
                                self._argent -= objet._cout_entretien
                                self._joueur.liste_tours[self._index_objet].entretient()  #creer une telle methode (score, points de vie...)
                            else :
                                F.blit("Argent non suffisant",self._dict_boutons[b][1][0])
'''
                                #utiliser ce qui suit
        		if clique_sur_bouton(construire): #avec objet dans case propre à menu
                T = Tour(pos_pix, self)
    		if T._cout_construction <= self._argent:
    			self._liste_tours.append(T)
    			self._argent -= T._cout_construction
    			self._carte[pos_x, pos_y] = 5
    			if pos_y>0:
    				self._carte[pos_x, pos_y-1] = 5
    		else:
    			print ("Vous n'avez pas suffisamment d'argent.")
                self.menu=None
'''
'''
    u avec bouton_dans_case
    def bouton_dans_case(self, clic_position):
        """ Retourne les coordonnees de la case de l'objet """
        pas_l = int(self.largeur/self.nb_cases_l)
        pas_h = int(self.hauteur/self.nb_cases_h)
        return (clic_position[0]//pas_l, clic_position[1]//pas_h)
    def positionner_objet(self, pos_case):
        a = int(pos_case[0]*self.largeur/self.nb_cases_l)
        b = int(pos_case[1]*self.hauteur/self.nb_cases_h)
        return (a, b)
'''
'''
    def interaction_tour():
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self.carte.objet_dans_case(event.pos)
            self._menu=enu("Tour",_liste_tours[i] tq _liste_tours[i].pos=pos_x, pos_y, pos_x,posy)
    		# PROPOSER AMELIORATION OU REPARATION
            print ("Amelioration ? Reparation ?")
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
'''
