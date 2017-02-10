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

class MenuJeu:
    def __init__(self):
        self._fenetre = pygame.display.set_mode((640, 360))
        image_menu = pygame.image.load("images/Menu/Menu_TD.jpg")\
        .convert_alpha()
        self._fenetre.blit(image_menu, (0, 0))
        self._etat = 0

    def maj_menu(self, event=None):
        if event != None and event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = event.pos
            if (pos_x >= 266 and pos_y>= 194 and pos_x < 394 and pos_y < 218):
                self._etat = "Jouer"
            elif (pos_x >= 288 and pos_y>= 240 and pos_x < 371 and pos_y < 261):
                self._etat = "Options"
            elif (pos_x >= 303 and pos_y>= 292 and pos_x < 352 and pos_y < 310):
                self._etat = "Quit"
    def maj_image(self):
        pos_x, pos_y = pygame.mouse.get_pos()
        if (pos_x >= 266 and pos_y>= 194 and pos_x < 394 and pos_y < 218):
            image_menu =pygame.image.load("images/Menu/Menu_TD_NewGame.jpg")\
            .convert_alpha()
            self._fenetre.fill((0,0,0))
            self._fenetre.blit(image_menu, (0,0))
        elif (pos_x >= 288 and pos_y>= 240 and pos_x < 371 and pos_y < 261):
            image_menu =pygame.image.load("images/Menu/Menu_TD_Options.jpg")\
            .convert_alpha()
            self._fenetre.fill((0,0,0))
            self._fenetre.blit(image_menu, (0,0))
        elif (pos_x >= 303 and pos_y>= 292 and pos_x < 352 and pos_y < 310):
                image_menu =pygame.image.load("images/Menu/Menu_TD_Quit.jpg")\
                .convert_alpha()
                self._fenetre.fill((0,0,0))
                self._fenetre.blit(image_menu, (0,0))
        else:
            image_menu =pygame.image.load("images/Menu/Menu_TD.jpg")\
            .convert_alpha()
            self._fenetre.fill((0,0,0))
            self._fenetre.blit(image_menu, (0,0))
        pygame.display.flip()

class Menu(object):
    def __init__(self, joueur, largeur):
        self._etat = None
        self._index_objet = None
        self._dict_infos= None
        self._joueur = joueur
        self.nb_cases_l = 50
        self.nb_cases_h = 6
        self.hauteur = 150
        self.largeur = largeur
        self._dict_boutons= None
        self._dernier_click = None
        self._dict_play = None
        self._etat_play = "play"

    def objet_dans_case(self, objet_position, C):
		""" Retourne les coordonnees de la case de l'objet """
		pas_l = int(self.largeur/self.nb_cases_l)
		pas_h = int(self.hauteur/self.nb_cases_h)
		return (objet_position[0]//pas_l, (objet_position[1]-\
        C.hauteur)//pas_h)

    def positionner_objet(self, pos_case, C):
		a = int(pos_case[0]*self.largeur/self.nb_cases_l)
		b = int(C.hauteur+pos_case[1]*\
        self.hauteur/self.nb_cases_h)
		return (a, b)

    def menu_statique(self, Vue, C):
        """ Affiche l'argent et le score du joueur """
        # Argent :
        pos_image = (0, C.hauteur+self.hauteur//5)
        image_or = pygame.image.load("images/interface/or1.png").convert_alpha()
        Vue._fenetre.blit(image_or, pos_image)
        font_or = pygame.font.Font(None, 50)
        or_joueur = str(self._joueur._argent)
        texte_or = font_or.render(or_joueur, 1, (255, 255, 0))
        Vue._fenetre.blit(texte_or, (60, pos_image[1]+5))

        # Score :
        pos_image = (0, C.hauteur+3*self.hauteur//5)
        image_score = pygame.image.load("images/interface/etoile.png")\
        .convert_alpha()
        Vue._fenetre.blit(image_score, pos_image)
        font_score = pygame.font.Font(None, 50)
        score_joueur = str(self._joueur._score)
        texte_score = font_score.render(score_joueur, 1, (0, 0, 255))
        Vue._fenetre.blit(texte_score, (60, pos_image[1]+5))

    def __contains__(self, position):
        lig, col = position
        return (lig >= 0) and (lig < self.nb_cases_l) and (col >= 0) \
    	and (col < self.nb_cases_h)

    def affichage_menu_haut(self, Affichage, C):
    	# Affichage des vies des bases
    	pos_vie = []
    	for i in range(len(C._pos_bases)):
    		pos_vie.append(C.positionner_objet((C.\
            nb_cases_l-len(C._pos_bases)+i, 0)))
    	for i in range(len(C._pos_bases)):
            b = C.get_base(i)
            if b._vie > b.vie_depart/2:
                Affichage.ajouter_element("images/interface/bases/hp_base.png"\
                , pos_vie[i], C)
            elif b._vie > b.vie_depart/5 and b._vie <= b.vie_depart/2:
                Affichage.ajouter_element("images/interface/bases/hp_base2.png"\
                , pos_vie[i], C)
            else:
                Affichage.ajouter_element("images/interface/bases/hp_base3.png"\
                , pos_vie[i], C)

        # Boutons play/pause
        pos_x, pos_y = pos_vie[0]
        pix_x = C.largeur/C.nb_cases_l
        pix_y = C.hauteur/C.nb_cases_h
        pos_y += pix_y
        self._dict_play = {
                        "images/interface/play.png":  (pos_x,pos_y),
                        "images/interface/playing.png":  (pos_x,pos_y),
                        "images/interface/pause.png": (pos_x+pix_x,pos_y),
                        "images/interface/pausing.png": (pos_x+pix_x,pos_y),
                        "images/interface/accelerate.png": (pos_x+2*pix_x,\
                        pos_y),
                        "images/interface/accelerating.png": (pos_x+2*pix_x,\
                        pos_y)
        }

        for d in self._dict_play.keys():
            if "ing" not in d:
                Affichage.ajouter_element(d, self._dict_play[d], C)


        for d in self._dict_play.keys():
            if self._etat_play == "play" and "playing" in d:
                Affichage.ajouter_element(d, self._dict_play[d], C)
            elif self._etat_play == "pause" and "pausing" in d:
                Affichage.ajouter_element(d, self._dict_play[d], C)
            elif self._etat_play == "accelerate" and "accelerating" in d:
                Affichage.ajouter_element(d, self._dict_play[d], C)

    def interaction_menu_haut(self, C, event=None):
        if event.type == MOUSEBUTTONDOWN and event.button==1:
            pos_x,pos_y = C.objet_dans_case(event.pos)
            for d in self._dict_play.keys():
                if (pos_x,pos_y) == C.objet_dans_case(self._dict_play[d]):
                    if "play" in d:
                        self._etat_play = "play"
                    elif "pause" in d:
                        self._etat_play = "pause"
                    elif "accelerate" in d:
                        self._etat_play = "accelerate"

                    return self._etat_play
        return None

    def maj_menu(self, event, C, Vue=None):
        if event !=None and event.type == MOUSEBUTTONDOWN and event.button==1:
            pos_x, pos_y = C.objet_dans_case(event.pos)
            if (pos_x,pos_y) in C and C.get_type_case((pos_x,pos_y)) == "tour":
                pos_case_tour = (pos_x, pos_y)
                for i in range(len(self._joueur.liste_tours)):
                    if pos_case_tour == C.objet_dans_case(self._joueur.\
                    liste_tours[i]._position):
                        self._index_objet = i
                self._etat = "tour"
                self._dernier_click = (pos_x, pos_y)
            elif (pos_x, pos_y) in C and C.get_type_case((pos_x, pos_y)) == \
            "place_construction":
                self._etat = "place_construction"
                self._dernier_click = (pos_x, pos_y)
            elif (pos_x, pos_y) in C and C.get_type_case((pos_x, pos_y)) \
            == "base":
                for i in range(len(C._pos_bases)):
                    if (pos_x,pos_y) == C._pos_bases[i]:
                        self._index_objet = i
                self._etat = "base"
                self._dernier_click = (pos_x, pos_y)
            elif (pos_x,pos_y) in C:
                self._etat = 0
                self._dict_infos = None
                self._dict_boutons = None

    def image(self, Vue, C):
        pos_image = self.positionner_objet((8,0), C)
        if self._etat == "tour" and self._index_objet!=None:
            # Le menu affiche l'image d'une tour
            image_tour = pygame.image.load("images/tours/tour"+str\
            (self._joueur.liste_tours[self._index_objet]._id_tour)+".png")\
            .convert_alpha()
            image_tour = pygame.transform.scale(image_tour, \
            (3*self.largeur/self.nb_cases_l, self.hauteur))
            Vue._fenetre.blit(image_tour, pos_image)
        if self._etat == "base" and self._index_objet!=None:
            name_image = "images/interface/bases/base_state1.png"
            b = C[self._dernier_click]
            if b.vie > b.vie_depart/5 and b._vie <= b.vie_depart/2:
                name_image = "images/interface/bases/base_state2.png"
            elif b.vie <= b.vie_depart/5:
                name_image = "images/interface/bases/base_state3.png"
            image_base = pygame.image.load(name_image).convert_alpha()
            image_base = pygame.transform.scale(image_base, \
            (3*self.largeur/self.nb_cases_l, self.hauteur))
            Vue._fenetre.blit(image_base, pos_image)

    def caracteristiques(self, Vue,C):
        if self._etat == "tour" and self._index_objet!=None:
            # Le menu affiche l'image d'une tour
            pos_vie=  self.positionner_objet((20,0.757), C)
            pos_degat= self.positionner_objet((20,1.61), C)
            pos_portee= self.positionner_objet((20,2.47), C)
            pos_cout_amelioration= self.positionner_objet((20,3.33), C)
            pos_cout_entretien= self.positionner_objet((20,4.185), C)
            pos_munitions = self.positionner_objet((20, 5.04), C)
            tour = self._joueur.liste_tours[self._index_objet]
            self._dict_infos = {
                            "vie : ":(pos_vie,tour._vie),
                            "degats : ":(pos_degat,tour.degat),
                            "portee : ":(pos_portee,tour.portee),
                            "couts d'amelioration : ":(pos_cout_amelioration,\
                            tour.cout_amelioration),
                            "couts d'entretien : ":(pos_cout_entretien,\
                            tour.cout_entretien),
                            "munitions : ":(pos_munitions, tour.munitions)
                            }
            if self._dict_infos != None :
                for d in self._dict_infos.keys():
                    font_donnee = pygame.font.Font(None, 30)
                    text_donnee = font_donnee.render(d+" "+str(\
                    self._dict_infos[d][1]), 1, (255, 255, 255))
                    Vue._fenetre.blit(text_donnee, self._dict_infos[d][0])

        if self._etat == "base" and self._index_objet != None :
            pos_vie= self.positionner_objet((20,0.5), C)
            pos_cout_entretien= self.positionner_objet((20,2.5), C)
            pos_cout_amelioration = self.positionner_objet((20,4.5), C)
            b = C.get_base(self._index_objet)
            self._dict_infos= {
                            "vie : ":(pos_vie,b._vie),
                            "couts d'entretien : ":(pos_cout_entretien, \
                            b._cout_entretien),
                            "couts d'amelioration : ":(pos_cout_amelioration, \
                            b._cout_amelioration)
                            }
            if self._dict_infos != None :
                for d in self._dict_infos.keys():
                    font_donnee = pygame.font.Font(None, 30)
                    text_donnee = font_donnee.render(d+" "+str(\
                    self._dict_infos[d][1]), 1, (255, 255, 255))
                    Vue._fenetre.blit(text_donnee, self._dict_infos[d][0])

    def boutons(self, Vue, C):
        if (self._etat == "tour" or self._etat == "base") and \
        self._index_objet != None:
            pos_bouton_ameliorer= self.positionner_objet((35,2), C)
            pos_bouton_entretenir= self.positionner_objet((45,2), C)
            if (self._etat == "tour"):
                elt = self._joueur.liste_tours[self._index_objet]
            elif (self._etat == "base"):
                elt = C.get_base(self._index_objet)

            self._dict_boutons = {
                               "amelioreraff":("images/interface/amelioration.png"\
                               ,pos_bouton_ameliorer),
                               "entretenir":("images/interface/reparation.png"\
                               ,pos_bouton_entretenir)
                                 }
            if Vue._joueur._argent < elt._cout_entretien:
                self._dict_boutons["entretenir"] = ("images/interface/"+"\
                reparation_indisponible.png",pos_bouton_entretenir)

            if Vue._joueur._argent < elt._cout_amelioration:
                self._dict_boutons["ameliorer"] = ("images/interface/"+"\
                amelioration_indisponible.png",pos_bouton_ameliorer)
            if self._dict_boutons != None :
                for b in self._dict_boutons.keys():
                    image = pygame.image.load(self._dict_boutons[b][0])\
                    .convert_alpha()
                    image = pygame.transform.scale(image, (3*self.largeur/\
                    self.nb_cases_l, 3*self.hauteur/self.nb_cases_h))
                    Vue._fenetre.blit(image, self._dict_boutons[b][1])

        if self._etat == "place_construction":
            liste_boutons_tour = []
            # A MODIFIER
            for i in range(3):
                liste_boutons_tour.append(self.positionner_objet(((2+i)\
                *self.nb_cases_l//5,1), C))
            self._dict_boutons = {}
            for i in range(3):
                if Vue._joueur._argent < ExtractIntFromFile("data_tourelle.csv"\
                ,i+1,3):
                    self._dict_boutons["tour"+str(i)] = ("images/tours/"+\
                    "construction_tour_indisponible.png", liste_boutons_tour[i])
                else:
                    self._dict_boutons["tour"+str(i)] = ("images/tours/"+\
                    "construction_tour"+str(i)+".png", liste_boutons_tour[i])

            if self._dict_boutons != None :
                for b in self._dict_boutons.keys():
                    image = pygame.image.load(self._dict_boutons[b][0])\
                    .convert_alpha()
                    image = pygame.transform.scale(image, (4*self.largeur/\
                    self.nb_cases_l, 4*self.hauteur/self.nb_cases_h))
                    Vue._fenetre.blit(image, self._dict_boutons[b][1])

    def interaction(self, event, Vue, C):
        if event != None and event.type == MOUSEBUTTONDOWN:
            pos_x, pos_y = event.pos
            pos_x, pos_y = self.objet_dans_case((pos_x, pos_y), C)
            if self._dict_boutons != None:
                if self._etat == "tour":
                    for b in self._dict_boutons.keys():
                        pos_boutton = self.objet_dans_case(\
                        self._dict_boutons[b][1], C)
                        if (pos_x,pos_y) in self and abs(pos_x-pos_boutton[0]\
                        -1)<3 and abs(pos_y-pos_boutton[1]-1)<3:
                            if b == "ameliorer":
                                self._joueur.ameliorer_tour(self._joueur.\
                                liste_tours[self._index_objet], Vue)
                            elif b == "entretenir":
                                self._joueur.reparer_tour(self._joueur.\
                                liste_tours[self._index_objet])
                if self._etat == "place_construction":
                    for b in self._dict_boutons.keys():
                        pos_boutton = self.objet_dans_case(\
                        self._dict_boutons[b][1], C)
                        if (pos_x,pos_y) in self and abs(pos_x-pos_boutton[0]\
                        -1)<4 and abs(pos_y-pos_boutton[1]-1)<4:
                            for i in range(3):
                                if b == "tour"+str(i):
                                    if self._joueur.construire_tour(i, \
                                    self._dernier_click, C) :
                                        self._etat = "tour"
