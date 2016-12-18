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

class Menu(object):
    def __init__(self, joueur):
        self._etat = None
        self._index_objet = None #reperer l'objetdans les attributs de joueur
        self._dict_infos= None
        self._joueur = joueur
        self.nb_cases_l = 50
        self.nb_cases_h = 6
        self.hauteur = 150
        self.largeur = self._joueur.carte.largeur
        self._dict_boutons= None
        self._dernier_click = None

    def objet_dans_case(self, objet_position):
		""" Retourne les coordonnees de la case de l'objet """
		pas_l = int(self.largeur/self.nb_cases_l)
		pas_h = int(self.hauteur/self.nb_cases_h)
		return (objet_position[0]//pas_l, (objet_position[1]-\
        self._joueur.carte.hauteur)//pas_h)

    def positionner_objet(self, pos_case):
		a = int(pos_case[0]*self.largeur/self.nb_cases_l)
		b = int(self._joueur.carte.hauteur+pos_case[1]*\
        self.hauteur/self.nb_cases_h)
		return (a, b)


    def affichage_menu_haut(self, Vue):
        """ Menu du haut de fenetre : Temps, Vie des bases, argent du joueur et son score """
        # Affichage du temps (Min:Sec)
        font_temps = pygame.font.Font(None, 36)
        temps = pygame.time.get_ticks()
        temps /= 1000
        secondes = temps%60
        minutes = temps//60
        text_temps = font_temps.render(str(minutes)+ " : "+ str(secondes), 1, (255, 255, 255))
        Vue._fenetre.blit(text_temps, (20,10))
        # Affichage des vies des bases
        pos_vie = []
        for i in range(len(Vue._bases)):
                pos_vie.append(self._joueur.carte.positionner_objet((self.nb_cases_l-len(self._bases)+i, 0)))
        for i, b in enumerate(self._bases):
        	if b._vie > b.vie_depart/2:
                       Vue.ajouter_element("images/interface/bases/hp_base.png", pos_vie[i])
        	elif b._vie > b.vie_depart/5 and b._vie <= b.vie_depart/2:
                       Vue.ajouter_element("images/interface/bases/hp_base2.png", pos_vie[i])
        	else:
                       Vue.ajouter_element("images/interface/bases/hp_base3.png", pos_vie[i])

    def menu_statique(self, Vue):
        """ Affiche l'argent et le score du joueur """
        # Argent :
        pos_image = (0, self._joueur.carte.hauteur+self.hauteur//5)
        image_or = pygame.image.load("images/interface/or1.png").convert_alpha()
        Vue._fenetre.blit(image_or, pos_image)
        font_or = pygame.font.Font(None, 50)
        or_joueur = str(self._joueur.argent)
        texte_or = font_or.render(or_joueur, 1, (255, 255, 0))
        Vue._fenetre.blit(texte_or, (60, pos_image[1]+5))

        # Score :
        pos_image = (0, self._joueur.carte.hauteur+3*self.hauteur//5)
        image_score = pygame.image.load("images/interface/etoile.png").convert_alpha()
        Vue._fenetre.blit(image_score, pos_image)
        font_score = pygame.font.Font(None, 50)
        score_joueur = str(self._joueur.score)
        texte_score = font_score.render(score_joueur, 1, (0, 0, 255))
        Vue._fenetre.blit(texte_score, (60, pos_image[1]+5))

    def __contains__(self, position):
        lig, col = position
        return (lig >= 0) and (lig < self.nb_cases_l) and (col >= 0) \
    	and (col < self.nb_cases_h)

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
        if event !=None and event.type == MOUSEBUTTONDOWN and event.button==1:
            pos_x, pos_y = self._joueur.carte.objet_dans_case(event.pos)
            if (pos_x,pos_y) in self._joueur.carte and self._joueur.carte.get_type_case((pos_x,pos_y)) == "tour":
                pos_case_tour = (pos_x, pos_y)
                for i in range(len(self._joueur.liste_tours)):
                    if pos_case_tour == self._joueur.carte.objet_dans_case(self._joueur.liste_tours[i]._position):
                        self._index_objet = i
                self._etat = "tour"
                self._dernier_click = (pos_x, pos_y)
            elif (pos_x, pos_y) in self._joueur.carte and self._joueur.carte.get_type_case((pos_x, pos_y)) == "place_construction":
                self._etat = "place_construction"
                self._dernier_click = (pos_x, pos_y)
            elif (pos_x,pos_y) in self._joueur.carte:
                self._etat = 0
                self._dict_infos = None
                self._dict_boutons = None

    def image(self, Vue):
        if self._etat == "tour" and self._index_objet!=None:
            # Le menu affiche l'image d'une tour
            pos_image = self.positionner_objet((8,0))
            image_tour = pygame.image.load("images/tours/tour"+str\
            (self._joueur.liste_tours[self._index_objet]._id_tour)+".png").convert_alpha()
            image_tour = pygame.transform.scale(image_tour, \
            (3*self.largeur/self.nb_cases_l, self.hauteur))
            Vue._fenetre.blit(image_tour, pos_image)

    def caracteristiques(self, Vue):
        if self._etat == "tour" and self._index_objet!=None:
            # Le menu affiche l'image d'une tour
            pos_vie=  self.positionner_objet((20,0.757))            #attributs
            pos_degat= self.positionner_objet((20,1.61))
            pos_portee= self.positionner_objet((20,2.47))
            pos_cout_amelioration= self.positionner_objet((20,3.33))
            pos_cout_entretien= self.positionner_objet((20,4.185))
            pos_munitions = self.positionner_objet((20, 5.04))
            tour = self._joueur.liste_tours[self._index_objet]
            self._dict_infos = {
                            "vie : ":(pos_vie,tour._vie),
                            "degats : ":(pos_degat,tour.degat),
                            "portee : ":(pos_portee,tour.portee),
                            "couts d'amelioration : ":(pos_cout_amelioration,tour.cout_amelioration),
                            "couts d'entretien : ":(pos_cout_entretien,tour.cout_entretien),
                            "munitions : ":(pos_munitions, tour.munitions)
                            }
            if self._dict_infos != None :
                for d in self._dict_infos.keys():
                    font_donnee = pygame.font.Font(None, 30)
                    text_donnee = font_donnee.render(d+" "+str(self._dict_infos[d][1]), 1, (255, 255, 255))
                    Vue._fenetre.blit(text_donnee, self._dict_infos[d][0])

    def boutons(self, Vue):
        if self._etat == "tour" and self._index_objet != None:
            pos_bouton_ameliorer= self.positionner_objet((35,2))
            pos_bouton_entretenir= self.positionner_objet((45,2))        # boutton12
            self._dict_boutons = {
                               "ameliorer":("images/interface/amelioration.png",pos_bouton_ameliorer),
                               "entretenir":("images/interface/reparation.png",pos_bouton_entretenir)
                               }
            if self._dict_boutons != None :
                for b in self._dict_boutons.keys():
                    image = pygame.image.load(self._dict_boutons[b][0]).convert_alpha()
                    image = pygame.transform.scale(image, (3*self.largeur/self.nb_cases_l, 3*self.hauteur/self.nb_cases_h))
                    Vue._fenetre.blit(image, self._dict_boutons[b][1])

        if self._etat == "place_construction":
            liste_boutons_tour = []
            # A MODIFIER
            for i in range(3):
                liste_boutons_tour.append(self.positionner_objet(((2+i)*self.nb_cases_l//5,1)))
            self._dict_boutons = {}
            for i in range(3):
                self._dict_boutons["tour"+str(i)] = ("images/tours/construction_tour"+str(i)+".png", liste_boutons_tour[i])
            if self._dict_boutons != None :
                for b in self._dict_boutons.keys():
                    image = pygame.image.load(self._dict_boutons[b][0]).convert_alpha()
                    image = pygame.transform.scale(image, (4*self.largeur/self.nb_cases_l, 4*self.hauteur/self.nb_cases_h))
                    Vue._fenetre.blit(image, self._dict_boutons[b][1])

    def interaction(self, event):
        if event != None and event.type == MOUSEBUTTONDOWN:
            pos_x, pos_y = event.pos
            pos_x, pos_y = self.objet_dans_case((pos_x, pos_y))
            if self._dict_boutons != None:
                if self._etat == "tour":
                    for b in self._dict_boutons.keys():
                        pos_boutton = self.objet_dans_case(self._dict_boutons[b][1])
                        if (pos_x,pos_y) in self and abs(pos_x-pos_boutton[0]-1)<3 and abs(pos_y-pos_boutton[1]-1)<3:
                            if b == "ameliorer":
                                self._joueur.ameliorer_tour(self._joueur.\
                                liste_tours[self._index_objet])
                            elif b == "entretenir":
                                self._joueur.reparer_tour(self._joueur.\
                                liste_tours[self._index_objet])
                if self._etat == "place_construction":
                    for b in self._dict_boutons.keys():
                        pos_boutton = self.objet_dans_case(self._dict_boutons[b][1])
                        if (pos_x,pos_y) in self and abs(pos_x-pos_boutton[0]-1)<4 and abs(pos_y-pos_boutton[1]-1)<4:
                            for i in range(3):
                                if b == "tour"+str(i):
                                    if self._joueur.construire_tour(i, self._dernier_click) :
                                        self._etat = "tour"




    def menu_place_construction(self, event, F):
        """ Affiche l'image, les caracteristiques (vie, degat) et les boutons"""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = self.objet_dans_case(event.pos)
            if self._joueur.carte.cases[pos_x][pos_y].type_objet == 102:
                self._etat="place"
                pos_image = (2*self.largeur/6, self.hauteur+self.hauteur/2) # image
                pos_vie=  (3*self.largeur/6, self.hauteur+150/6)            #attributs
                pos_degat= (3*self.largeur/6, self.hauteur+150/6*2)
                pos_portee= (3*self.largeur/6, self.hauteur+150/6*3)
                pos_cout_amelioration= (3*self.largeur/6, self.hauteur+150/6*4)
                pos_cout_entretien= (3*self.largeur/6, self.hauteur+150/6*5)
                pos_bouton_ameliorer=(5*self.largeur/6, self.hauteur+150/3)
                pos_bouton_entretenir=(5*self.largeur/6, self.hauteur+150/3*2)       # boutton
                #Creer une tout virtuelle pour avoir les infos avant
                self._dict_infos = {
                                "vie : ":(pos_vie,tour._vie),
                                "degats : ":(pos_degat,tour._degat),
                                "portee : ":(pos_portee,tour._portee),
                                "couts d'amelioration : ":(pos_cout_amelioration,tour._cout_amelioration),
                                "couts d'entretien : ":(pos_cout_entretien,tour._cout_entretien)}
                self._dict_boutons = {"construire":("/images/interface/amelioration.png",pos_bouton_ameliorer)}

                image_tour = pygame.image.load("images/tours/tour.png").convert_alpha()
                F.blit(image_tour, pos_image)

                for d in self._dict_infos.keys():
                    font_donnee = pygame.font.Font(None, 20)
            	    text_donnee = font_donnee.render(d, 1, (255, 255, 255))
                    F.blit(text_donnee, self._dict_infos[d])
                for b in self._dict_boutons.keys():
                    image = pygame.image.load(self._dict_boutons[b][0]).convert_alpha()
                    F.blit(self._dict_boutons[b][0], self._dict_boutons[b][1])

        if event.type == MOUSEBUTTONDOWN and event.button == 1 and type_objet==5:
            pos_x, pos_y = self.objet_dans_case(event.pos)
            pos = (pos_x,pos_y)
            for b in self._dict_boutons.keys():
                if ((pos[0]>=self._dict_boutons[b][1][0])and(pos[0]<=self._dict_boutons[b][1][0]+2000)):
                    if ((pos[1]>=self._dict_boutons[b][1][1])and(pos[1]<=self._dict_boutons[b][1][1]+150/3)):
                        if (self._dict_boutons[b][0]=="ameliorer"):
                            objet=self._joueur.liste_tours[self._index_objet]
                            if objet._cout_amelioration<=self._joueur.argent:
                                self._argent -= objet._cout_amelioration
                                self._joueur.liste_tours[self._index_objet].ameliore()
                            else :
                                F.blit("Argent non suffisant",self._dict_boutons[b][1][0])
                        if (self._dict_boutons[b][0]=="entretenir"):
                            objet=self._joueur.liste_tours[self._index_objet]
                            if objet._cout_entretien<=self._joueur.argent:
                                self._argent -= objet._cout_entretien
                                self._joueur.liste_tours[self._index_objet].entretient()  #creer une telle methode (score, points de vie...)
                            else :
                                F.blit("Argent non suffisant",self._dict_boutons[b][1][0])
