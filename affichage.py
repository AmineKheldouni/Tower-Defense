#!/usr/bin/python
#encoding: utf8

from joueur import *
from menu import *
from excel import *
from menu import *


class Affichage_fenetre:
	def __init__(self, joueur):
		self.dico_carte=cree_dico('legend',1,2)
		self.dico_carte_object=cree_dico('legend2',1,2)
		self.projectile = []
		self._listenoms_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._joueur = joueur
		self._menu = Menu(self._joueur)
		self._fenetre = pygame.display.set_mode((self.carte.largeur, self.carte.hauteur+self._menu._hauteur))	# A MODIFIER
		pygame.display.set_caption("Tower Defense")
		self._nb_decor = [5, 5] # 10 Rochers, 5 Arbres
		self._bases = []
		liste_x = [self.carte.nb_cases_l//10+3, (2*self.carte.nb_cases_l//5+3*self.carte.nb_cases_l//5)//2, 4*self.carte.nb_cases_l//5-2]
		for x in liste_x:
			pos_base = self.carte.positionner_objet((x, 0))
			self._bases.append(Base(pos_base, self._joueur))
		self._places_construction = []
		for i in range(self.carte.nb_cases_l):
			for j in range(self.carte.nb_cases_h):
				if extract_carte(self._joueur.carte._id_carte+"_objets", i+1, j+1) == 102:
					self._places_construction.append((i, j))

		self._chemin = []

	@property
	def carte(self):
		return self._joueur._carte

	@property
	def joueur(self):
		return self._joueur

	def ajouter_element(self, nom_image, position):
		element = pygame.image.load(nom_image).convert_alpha()
		if not "background" in nom_image and not "GameOver" in nom_image \
		and not "menu_bas" in nom_image and not "balle" in nom_image:
			element = pygame.transform.scale(element, (self.carte.largeur/self.carte.nb_cases_l, self.carte.hauteur/self.carte.nb_cases_h))

		if "balle" in nom_image:
			element = pygame.transform.smoothscale(element, (self.carte.largeur/self.carte.nb_cases_l, self.carte.hauteur/self.carte.nb_cases_h))

		if "tour" in nom_image or "arbre" in nom_image or "base_state1" in nom_image or "Aquadragon" in nom_image:
			element = pygame.transform.scale(element, (self.carte.largeur/self.carte.nb_cases_l, 2*self.carte.hauteur/self.carte.nb_cases_h))
			self._fenetre.blit(element, (position[0], position[1]-\
			self.carte.hauteur/self.carte.nb_cases_h))
		else:
			self._fenetre.blit(element, position)


	def formation_chemin(self):
		for j in range(self.carte.nb_cases_l):
			for i in range(self.carte.nb_cases_h):
				value_case=extract_carte(self.carte.id_carte,i+1,j+1)
				if(value_case==1)or((value_case)==2):
					pos= self.carte.positionner_objet((j,i))
					self._chemin.append(pos)

	def affichage_terrain(self):
		self.ajouter_element("images/interface/background2.jpg", (0, 0))

	def affichage_carte(self, carte):
		for j in range(carte.nb_cases_l):
			for i in range(carte.nb_cases_h):
				value_case=extract_carte(carte.id_carte,i+1,j+1)
				pos = carte.positionner_objet((j,i))
				if(value_case!=0):
					self.ajouter_element(self.dico_carte[value_case], pos)
				if ((carte._objets[j][i]._id_excel)!=0):
					graphic = self.dico_carte_object[carte._objets[j][i]._id_excel]
					self.ajouter_element(graphic, pos)

	def affichage_chemin(self):
		# Affichage chemin :
		for position_chemin in self._chemin:
			pos = self.carte.objet_dans_case(position_chemin)
			self.ajouter_element("images/map_tile/route3.png", position_chemin)
			self._joueur._carte[pos] = "chemin"

	def affichage_portee(self):
		pos = pygame.mouse.get_pos()
		pos_case = self.carte.objet_dans_case(pos)
		if self.carte[pos_case] == "tour" :
			tmp = self.carte.objet_dans_case(pos)
			pos = self.carte.positionner_objet(tmp)
			for T in self._joueur.liste_tours:
				if T._position == pos:
					pos = self.carte.positionner_objet((tmp[0]+0.5, tmp[1]+0.5))
					pygame.draw.circle(self._fenetre, (255, 255, 255), (int(pos[0]), int(pos[1])), T._portee, 2)

	def affichage_statique(self):
		# Affichage bases :
		for b in self._bases:
			if b._vie > b.vie_depart/2:
				self.ajouter_element("images/interface/bases/base_state1.png", b.position)
			elif b._vie >b.vie_depart/5 and b._vie <=b.vie_depart/2:
				self.ajouter_element("images/interface/bases/base_state2.png", b.position)
			else:
				self.ajouter_element("images/interface/bases/base_state3.png", b.position)
			self._joueur._carte[self.carte.objet_dans_case(b._position)] = "base"

		for T in self.joueur.liste_tours:
			self.ajouter_element(self._listenoms_tours[T._id_tour], T._position)

	def affiche_soldat(self,soldat):
		self.ajouter_element("images/armee/"+soldat._graphic+"/"+soldat._graphic+soldat.dir_to_graph()+".png",soldat._position)

	def affichage_armee(self, armee):
		for b in self._bases:
			for soldat in armee._liste_soldat:
				if not soldat._is_dead and soldat._position != b._position:
					type_soldat = soldat._type_soldat
					anim_soldat = soldat._animation
					soldat.arriver_base(self._bases)
					self.affiche_soldat(soldat)

	def affichage_projectile(self, projectile):
		# im_projectile = pygame.image.load("images/tours/balle.png").convert_alpha()
		if projectile._position != projectile._arrivee:
			self.ajouter_element("images/tours/balle.png",projectile._position)

	def gestion_menu(self):
		""" Nouvelle gestion du Menu avec la classe Menu """
		pos_menu = self.carte.positionner_objet((0, self.carte.nb_cases_h))
		self.ajouter_element("images/interface/menu_bas2.jpg", pos_menu)
		self._menu.affichage_menu_haut(self)
		self._menu.menu_statique(self)

	def affichage_menu(self, armee):
		pos_menu = self.carte.positionner_objet((0, 14))
		self.ajouter_element("images/interface/menu_bas2.jpg", pos_menu)
		font_menu = pygame.font.Font(None, 36)
		text_menu=font_menu.render("Menu d'Objet",1,(255,255,255))
		self._fenetre.blit(text_menu,(0,self.carte.hauteur))
		pos = pygame.mouse.get_pos()
		pos_case = self.carte.objet_dans_case(pos)
		if self.carte[pos_case] == "tour" :
                        self.ajouter_element("images/tours/tour2.png", (self.carte.largeur//4,self.carte.hauteur+50))
                        tmp = self.carte.objet_dans_case(pos)
			pos = self.carte.positionner_objet(tmp)
			for T in self._joueur.liste_tours:
				if T._position == pos:
                                        text_tour=font_menu.render("Tour : niveau de vie = "+str(T._vie),1,(255,0,0))
                                        self._fenetre.blit(text_tour,(self.carte.largeur//4 + 55, self.carte.hauteur+50))

                if self.carte[pos_case]=="base":
                        self.ajouter_element("images/interface/bases/base_state1.png", (self.carte.largeur//4,self.carte.hauteur+50))
                        tmp = self.carte.objet_dans_case(pos)
			pos = self.carte.positionner_objet(tmp)
			for T in self._bases:
				if T._position == pos:
                                        text_base=font_menu.render("Base : niveau de vie = "+str(T._vie),1,(255,0,0))
                                        self._fenetre.blit(text_base,(self.carte.largeur//4 + 55, self.carte.hauteur+50))
                for soldat in armee._liste_soldat:
                        if ((soldat._position[0]>=pos[0]-50) and (soldat._position[0]<=pos[0]+50) and (soldat._ancienne_position[1]>=pos[1]-50) and (soldat._ancienne_position[1]<=pos[1]+50) or ((soldat._ancienne_position[0]>=pos[0]-50) and (soldat._ancienne_position[0]<=pos[0]+50) and (soldat._ancienne_position[1]>=pos[1]-50) and (soldat._ancienne_position[1]<=pos[1]+50)) ):
                                self.ajouter_element("images/armee/boss/boss_bas.png", (self.carte.largeur//4,self.carte.hauteur+50))
                                text_base=font_menu.render("soldat:"+str(soldat._vie),1,(255,255,255))
                                self._fenetre.blit(text_base,(self.carte.largeur//4 + 50, self.carte.hauteur+50))
