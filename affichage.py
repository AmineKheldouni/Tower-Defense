#!/usr/bin/python
#encoding: utf8

from joueur import *
from menu import *
from csvuser import *

class Affichage_fenetre:
	def __init__(self, joueur):
		self.dico_carte=DicoFromFile("cartes_legend.csv",2,7,1,2)
		self.dico_carte_object=DicoFromFile("cartes_legend2.csv",2,16,1,2)
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._joueur = joueur
		self._menu = Menu(self._joueur)
		self._fenetre = pygame.display.set_mode((self.carte.largeur, self.carte.hauteur+self._menu.hauteur), pygame.RESIZABLE)	# A MODIFIER
		self._scale_l = self.carte.largeur/self.carte.nb_cases_l
		self._scale_h = self.carte.hauteur/self.carte.nb_cases_h
		pygame.display.set_caption("Tower Defense")

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
			element = pygame.transform.scale(element, (self._scale_l, self._scale_h))
		if "tour" in nom_image or "arbre" in nom_image or "base_state1" in nom_image:
			#element = pygame.transform.scale(element, (self.carte.largeur/self.carte.nb_cases_l, 2*self.carte.hauteur/self.carte.nb_cases_h))
			self._fenetre.blit(element, (position[0], position[1]-\
			2.35*self.carte.hauteur/self.carte.nb_cases_h))
		else:
			self._fenetre.blit(element, position)

	def affichage_terrain(self):
		self.ajouter_element("images/interface/background2.jpg", (0, 0))

	def affichage_carte(self,carte):
		""" affiche tapis des cases (chemin par exemple)"""
		for j in range(carte.nb_cases_l):
			for i in range(carte.nb_cases_h):
				value_case=carte._cases[j][i]._tapis
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
		dir_voisin = soldat._voisins[soldat._direction]
		pos_carte = self._joueur.carte.positionner_objet(soldat._position)
		pos_x=pos_carte[0] + dir_voisin[0]*((soldat._pas-50)*self._scale_l)/100
		pos_y=pos_carte[1] + dir_voisin[1]*((soldat._pas-50)*self._scale_h)/100
		self.ajouter_element("images/armee/"+soldat._graphic+"/"+soldat._graphic+soldat.dir_to_graph()+".png",(pos_x,pos_y))
		self.affiche_etat(soldat._etat, (pos_x,pos_y))

	def affiche_etat(self,etat, pos_pix):
		if(etat._nom != "0"):
			self.ajouter_element("images/etat/"+(etat._nom)+"/"+"0.png",pos_pix)

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

	def gestion_menu_statique(self):
		pos_menu = self.carte.positionner_objet((0, self.carte.nb_cases_h))
		self.ajouter_element("images/interface/Menubas/menu_bas3.png", pos_menu)
		self._menu.affichage_menu_haut(self)
		self._menu.menu_statique(self)

	def gestion_menu(self, event=None):
		""" Nouvelle gestion du Menu avec la classe Menu """
		self.gestion_menu_statique()
		self._menu.maj_menu(event, self)
		self._menu.image(self)
		self._menu.caracteristiques(self)
		self._menu.boutons(self)
		self._menu.interaction(event, self)

	def animation_amelioration(self, elt):
		for i in range(5):
			pygame.time.wait(50)
			if i<=2:
				self.ajouter_element("images/tours/tour"+\
				str(elt._id_tour)+"amelioration"+\
				str(i+1)+".png",elt._position)
			else:
				self.ajouter_element("images/tours/tour"+\
				str(elt._id_tour)+"amelioration"+\
				str(5-i)+".png",elt._position)
			pygame.display.flip()

	def affiche_all(self,Carte,Arme):
		self.affichage_terrain()
		self.affichage_carte(Carte)
		self.affichage_armee(Arme)
		self._menu.affichage_menu_haut(self)
		self.affiche_carte_objet(Carte)
		self.affichage_portee()
