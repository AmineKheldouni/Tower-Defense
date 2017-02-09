#!/usr/bin/python
#encoding: utf8

from joueur import *
from menu import *
from csvuser import *

class Affichage_fenetre:
	def __init__(self, joueur, C):
		self.dico_carte=DicoFromFile("cartes_legend.csv",2,7,1,2)
		self.dico_carte_object=DicoFromFile("cartes_legend2.csv",2,16,1,2)
		self._tableau_type_armee = [1] 
		self._joueur = joueur
		self._menu = Menu(self._joueur, C.largeur)
		self._fenetre = pygame.display.set_mode((C.largeur, C.hauteur+self._menu.hauteur),\
		 pygame.RESIZABLE)	# A MODIFIER
		self._scale_l = C.largeur/C.nb_cases_l
		self._scale_h = C.hauteur/C.nb_cases_h
		pygame.display.set_caption("Tower Defense")

	@property
	def joueur(self):
		return self._joueur

	def ajouter_element(self, nom_image, position, C):
		element = pygame.image.load(nom_image).convert_alpha()
		if not "background" in nom_image and not "GameOver" in nom_image \
		and not "menu_bas" in nom_image and not "balle" in nom_image and \
		not "arbre" in nom_image and not "tour" in nom_image and not \
		"base_state1" in nom_image:
			element = pygame.transform.scale(element, (self._scale_l, self._scale_h))
		if "tour" in nom_image or "arbre" in nom_image or "base_state1" in nom_image:
			self._fenetre.blit(element, (position[0], position[1]-\
			2.35*C.hauteur/C.nb_cases_h))
		else:
			self._fenetre.blit(element, position)

	def affichage_terrain(self, C):
		self.ajouter_element("images/interface/background2.jpg", (0, 0), C)

	def affichage_carte(self,carte):
		""" affiche tapis des cases (chemin par exemple)"""
		for x in range(carte.nb_cases_h):
			for y in range(carte.nb_cases_l):
				value_case=carte[(x,y)]._tapis
				pos = carte.positionner_objet((x,y))
				if(value_case!=0):
					self.ajouter_element(self.dico_carte[value_case],pos, carte)

	def affiche_carte_objet(self,carte):
		for x in range(carte.nb_cases_h):
			for y in range(carte.nb_cases_l):
				pos = carte.positionner_objet((x,y))
				if(carte[(x,y)]._id_graphic !=0 ):
					graphic = self.dico_carte_object[carte[x,y]._id_graphic]
					if(graphic !="None"):
						self.ajouter_element(graphic, pos, carte)

	def affichage_portee(self,C):
		pos = pygame.mouse.get_pos()
		pos_case = C.objet_dans_case(pos)
		if pos_case in C and C.get_type_case(pos_case) == "tour" :
			tmp = C.objet_dans_case(pos)
			pos = C.positionner_objet(tmp)
			for T in self._joueur.liste_tours:
				if T._position == pos:
					pos = C.positionner_objet((tmp[0]+0.5, tmp[1]+0.5))
					pygame.draw.circle(self._fenetre, (255, 255, 255), (int(pos[0]), \
					int(pos[1])), T._portee*self._scale_l, 2)

	def affiche_soldat(self,soldat, C):
		dir_voisin = soldat._voisins[soldat._direction]
		pos_carte = C.positionner_objet(soldat._position)
		pos_x=pos_carte[0] + dir_voisin[0]*((soldat._pas-50)*self._scale_l)/100
		pos_y=pos_carte[1] + dir_voisin[1]*((soldat._pas-50)*self._scale_h)/100
		self.ajouter_element("images/armee/"+soldat._graphic+"/"+soldat._graphic+\
		soldat.dir_to_graph()+".png",(pos_x,pos_y), C)
		self.affiche_etat(soldat._etat, (pos_x,pos_y), C)

	def affiche_etat(self,etat, pos_pix, C):
		if(etat._nom != "0"):
			self.ajouter_element("images/etat/"+(etat._nom)+"/"+"0.png",pos_pix, C)

	def affichage_armee(self, armee, C):
		for soldat in armee._liste_soldat:
			if not soldat._is_dead:
				type_soldat = soldat._type_soldat
				anim_soldat = soldat._animation
				self.affiche_soldat(soldat, C)

	def affichage_projectile(self, projectile, C):
		# im_projectile = pygame.image.load("images/tours/balle.png").convert_alpha()
		if projectile._position != projectile._arrivee:
			self.ajouter_element("images/tours/balle.png",projectile._position, C)

	def gestion_menu_statique(self, C):
		pos_menu = C.positionner_objet((0, C.nb_cases_h))
		self.ajouter_element("images/interface/Menubas/menu_bas3.png", pos_menu, C)
		self._menu.affichage_menu_haut(self, C)
		self._menu.menu_statique(self, C)

	def gestion_menu(self, C, event=None):
		""" Nouvelle gestion du Menu avec la classe Menu """
		self.gestion_menu_statique(C)
		self._menu.maj_menu(event, C, self)
		self._menu.image(self, C)
		self._menu.caracteristiques(self, C)
		self._menu.boutons(self, C)
		self._menu.interaction(event, self, C)

	def animation_amelioration(self, elt):
		for i in range(5):
			pygame.time.wait(50)
			if i<=2:
				self.ajouter_element("images/tours/tour"+\
				str(elt._id_tour)+"amelioration"+\
				str(i+1)+".png",elt._position, C)
			else:
				self.ajouter_element("images/tours/tour"+\
				str(elt._id_tour)+"amelioration"+\
				str(5-i)+".png",elt._position, C)
			pygame.display.flip()


	def affiche_score(self, C, player="", score =-1):
		self._fenetre.fill((0,0,0))
		font =  pygame.font.Font("Blacksword.otf",30)
		font_titre = pygame.font.Font("Blacksword.otf",60)
		font_soustitre = pygame.font.Font("Blacksword.otf",40)
		h = C.hauteur+self._menu.hauteur
		l = C.largeur
		scores = give_score()
		txt = font_titre.render("Top 10 des meilleurs scores" ,1, (255, 255, 255))
		self._fenetre.blit(txt,(2.5*l/6,h/15))
		txt = font_soustitre.render("Classement" ,1, (255, 255, 255))
		self._fenetre.blit(txt,(l/6,3*h/15))
		txt = font_soustitre.render("Pseudo" ,1, (255, 255, 255))
		self._fenetre.blit(txt,(2*l/6,3*h/15))
		txt = font_soustitre.render("Score" ,1, (255, 255, 255))
		self._fenetre.blit(txt,(5*l/6,3*h/15))
		for i  in range(len(scores)):
			if player == scores[i][1] and score == scores[i][2]:
				a=1
			else:
				a=255
			txt = font.render(str(scores[i][0]), 1, (255, a, 255))
			self._fenetre.blit(  txt,  (l/6, (i+4)*h/15))
			txt = font.render(str(scores[i][1]), 1, (255, a, 255))
			self._fenetre.blit(  txt,  (2*l/6, (i+4)*h/15))
			txt = font.render(str(scores[i][2]), 1, (255, a, 255))
			self._fenetre.blit(  txt,  (5*l/6, (i+4)*h/15))


	def affiche_all(self,Carte,Arme):
		self.affichage_terrain(Carte)
		self.affichage_carte(Carte)
		self.affichage_armee(Arme, Carte)
		self._menu.affichage_menu_haut(self,Carte)
		self.affiche_carte_objet(Carte)
		self.affichage_portee(Carte)
