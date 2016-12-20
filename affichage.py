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
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._joueur = joueur
		self._menu = Menu(self._joueur)
		self._fenetre = pygame.display.set_mode((self.carte.largeur, self.carte.hauteur+self._menu.hauteur), pygame.RESIZABLE)	# A MODIFIER
		pygame.display.set_caption("Tower Defense")
		self._bases = []
		liste_x = [self.carte.nb_cases_l//10+3, (2*self.carte.nb_cases_l//5+3*self.carte.nb_cases_l//5)//2, 4*self.carte.nb_cases_l//5-2]

	@property
	def carte(self):
		return self._joueur._carte

	@property
	def joueur(self):
		return self._joueur

	def ajouter_element(self, nom_image, position):
		element = pygame.image.load(nom_image).convert_alpha()
		if not "background" in nom_image and not "GameOver" in nom_image \
		and not "menu_bas" in nom_image and not "balle" in nom_image and \
		not "arbre" in nom_image and not "tour" in nom_image and not \
		"base_state1" in nom_image:
			element = pygame.transform.scale(element, (self.carte.largeur/self.carte.nb_cases_l, self.carte.hauteur/self.carte.nb_cases_h))


		if "tour" in nom_image or "arbre" in nom_image or "base_state1" in nom_image or "Aquadragon" in nom_image:
			#element = pygame.transform.scale(element, (self.carte.largeur/self.carte.nb_cases_l, 2*self.carte.hauteur/self.carte.nb_cases_h))
			self._fenetre.blit(element, (position[0], position[1]-\
			2.35*self.carte.hauteur/self.carte.nb_cases_h))
		else:
			self._fenetre.blit(element, position)

	def affichage_terrain(self):
		self.ajouter_element("images/interface/background2.jpg", (0, 0))

	def affichage_carte(self,carte):
		for j in range(carte.nb_cases_l):
			for i in range(carte.nb_cases_h):
				value_case=carte._cases[j][i].tapis
				pos = carte.positionner_objet((j,i))
				if(value_case!=0):
					self.ajouter_element(self.dico_carte[value_case],pos)

	def affiche_carte_objet(self,carte):
		for j in range(carte.nb_cases_l):
			for i in range(carte.nb_cases_h):
				pos = carte.positionner_objet((j,i))
				if((carte._cases[j][i])._id_graphic !=0 ):
					graphic = self.dico_carte_object[(carte._cases[j][i])._id_graphic]
					if(graphic !="None"):
						self.ajouter_element(graphic, pos)

	def affichage_portee(self):
		pos = pygame.mouse.get_pos()
		pos_case = self.carte.objet_dans_case(pos)
		if pos_case in self._joueur.carte and self.carte.get_type_case(pos_case) == "tour" :
			tmp = self.carte.objet_dans_case(pos)
			pos = self.carte.positionner_objet(tmp)
			for T in self._joueur.liste_tours:
				if T._position == pos:
					pos = self.carte.positionner_objet((tmp[0]+0.5, tmp[1]+0.5))
					pygame.draw.circle(self._fenetre, (255, 255, 255), (int(pos[0]), int(pos[1])), T._portee, 2)

	def affiche_soldat(self,soldat):
		pos_carte = self._joueur.carte.positionner_objet(soldat._position)
		self.ajouter_element("images/armee/"+soldat._graphic+"/"+soldat._graphic+soldat.dir_to_graph()+".png",pos_carte)

	def affichage_armee(self, armee):
		for soldat in armee._liste_soldat:
			if not soldat._is_dead:
				type_soldat = soldat._type_soldat
				anim_soldat = soldat._animation
				self.affiche_soldat(soldat)

	def affichage_projectile(self, projectile):
		# im_projectile = pygame.image.load("images/tours/balle.png").convert_alpha()
		if projectile._position != projectile._arrivee:
			self.ajouter_element("images/tours/balle.png",projectile._position)

	def gestion_menu(self, event=None):
		""" Nouvelle gestion du Menu avec la classe Menu """
		pos_menu = self.carte.positionner_objet((0, self.carte.nb_cases_h))
		self.ajouter_element("images/interface/menu_bas2.jpg", pos_menu)
		self._menu.affichage_menu_haut(self)
		self._menu.menu_statique(self)
		self._menu.maj_menu(event, self)
		self._menu.image(self)
		self._menu.caracteristiques(self)
		self._menu.boutons(self)
		self._menu.interaction(event)
