#!/usr/bin/python
#encoding: utf8

from joueur import *
from menu import *
class Affichage_fenetre:
	def __init__(self, joueur):
		self.projectile = []
		self._listenoms_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._listenoms_soldats = [[["images/armee/boss/boss_bas.png", "images/armee/boss/boss_bas_pd.png", "images/armee/boss/boss_bas_pg.png"], ["images/armee/boss/boss_gauche.png", "images/armee/boss/boss_gauche_pd.png", "images/armee/boss/boss_gauche_pg.png"], ["images/armee/boss/boss_haut.png", "images/armee/boss/boss_haut_pd.png", "images/armee/boss/boss_haut_pg.png"], ["images/armee/boss/boss_droite.png", "images/armee/boss/boss_droite_pd.png", "images/armee/boss/boss_droite_pg.png"]]]
		self._joueur = joueur
		self._fenetre = pygame.display.set_mode((self.carte.largeur, self.carte.hauteur+150))	# A MODIFIER
		self._nb_decor = [5, 5] # 10 Rochers, 5 Arbres
		self._liste_rochers = []
		self._liste_arbre = []
		self._bases = []
		liste_x = [self.carte.nb_cases_l//10+3, (2*self.carte.nb_cases_l//5+3*self.carte.nb_cases_l//5)//2, 4*self.carte.nb_cases_l//5-2]
		for x in liste_x:
			pos_base = self.carte.positionner_objet((x, 0))
			self._bases.append(Base(pos_base, self._joueur))
		self._places_construction = [(11,10), (16, 10), (4, 2)] # A MODIFIER
		self._chemin = []

	@property
	def carte(self):
		return self._joueur._carte

	@property
	def joueur(self):
		return self._joueur
	def ajouter_element(self, nom_image, position):
		element = pygame.image.load(nom_image).convert_alpha()
		if "tour" in nom_image or "arbre" in nom_image or "base_state1" in nom_image:
			self._fenetre.blit(element, (position[0], position[1]-\
			self.carte.hauteur/self.carte.nb_cases_h))
		else:
			self._fenetre.blit(element, position)

	def genere_decor(self):
		for i in range(self._nb_decor[0]):
			tmp1, tmp2 = np.random.randint(self.carte.nb_cases_l-1), np.random.randint(1, self.carte.nb_cases_h-1)
			while self.carte[tmp1, tmp2] != "herbe":
				tmp1, tmp2 = np.random.randint(self.carte.nb_cases_l-1), np.random.randint(self.carte.nb_cases_h-1)
			pos_x, pos_y = self.carte.positionner_objet((tmp1,tmp2))
			self._joueur._carte[tmp1, tmp2] = "decor" # La case devient un decor
			self._liste_rochers.append((pos_x, pos_y))
		for i in range(self._nb_decor[1]):
			tmp1, tmp2 = np.random.randint(self.carte.nb_cases_l-1), np.random.randint(1, self.carte.nb_cases_h-1)
			while self.carte[tmp1, tmp2] != "herbe":
				tmp1, tmp2 = np.random.randint(self.carte.nb_cases_l-1), np.random.randint(self.carte.nb_cases_h-1)
			pos_x, pos_y = self.carte.positionner_objet((tmp1,tmp2))
			self._joueur._carte[tmp1, tmp2] = "decor" # La case devient un decor
			self._liste_arbre.append((pos_x, pos_y))

	def formation_chemin(self):
		for j in range(self.carte.nb_cases_h//2, self.carte.nb_cases_h):
			pos = (self.carte.nb_cases_l//5, j)
			pos2 = (self.carte.nb_cases_l*2//5, j)
			pos3 = (self.carte.nb_cases_l*3//5, j)
			pos4 = (self.carte.nb_cases_l*4//5, j)
			pos = self.carte.positionner_objet(pos)
			pos2 = self.carte.positionner_objet(pos2)
			pos3 = self.carte.positionner_objet(pos3)
			pos4 = self.carte.positionner_objet(pos4)
			self._chemin.append(pos)
			self._chemin.append(pos2)
			self._chemin.append(pos3)
			self._chemin.append(pos4)
		for i in range(1, self.carte.nb_cases_l-1):
			pos = (i, self.carte.nb_cases_h//2)
			pos = self.carte.positionner_objet(pos)
			self._chemin.append(pos)
		pos = self.carte.positionner_objet((1, self.carte.nb_cases_h//2-1))
		self._chemin.append(pos)
		pos = self.carte.positionner_objet((self.carte.nb_cases_l-2, self.carte.nb_cases_h//2-1))
		self._chemin.append(pos)
		for i in range(1, self.carte.nb_cases_l-1):
			pos = (i, self.carte.nb_cases_h//2-2)
			pos = self.carte.positionner_objet(pos)
			self._chemin.append(pos)
		for j in range(1, self.carte.nb_cases_h//2-3):
			pos = (self.carte.nb_cases_l//2, j)
			pos = self.carte.positionner_objet(pos)
			self._chemin.append(pos)

		liste_x = [self.carte.nb_cases_l//10, 2*self.carte.nb_cases_l//5, 3*self.carte.nb_cases_l//5,  4*self.carte.nb_cases_l//5]
		for x in liste_x:
			self._chemin.append(self.carte.positionner_objet((x, self.carte.nb_cases_h//2-3)))
		y = self.carte.nb_cases_h//2-4
		for x in range(self.carte.nb_cases_l//10, self.carte.nb_cases_l//10+3):
			self._chemin.append(self.carte.positionner_objet((x, y)))
		for x in range(2*self.carte.nb_cases_l//5, 3*self.carte.nb_cases_l//5+1):
			self._chemin.append(self.carte.positionner_objet((x, y)))
		for x in range(4*self.carte.nb_cases_l//5-1, 4*self.carte.nb_cases_l//5+1):
			self._chemin.append(self.carte.positionner_objet((x, y)))

		liste_x = [self.carte.nb_cases_l//10+3, (2*self.carte.nb_cases_l//5+3*self.carte.nb_cases_l//5)//2, 4*self.carte.nb_cases_l//5-2]
		for x in liste_x:
			for j in range(0, self.carte.nb_cases_h//2-3):
				self._chemin.append(self.carte.positionner_objet((x, j)))

	def affichage_terrain(self):
		self.ajouter_element("images/interface/background2.jpg", (0, 0))

	def affichage_chemin(self):
		# Affichage chemin :
		for position_chemin in self._chemin:
			pos = self.carte.objet_dans_case(position_chemin)
			self.ajouter_element("images/interface/route3.png", position_chemin)
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
				self.ajouter_element("images/interface/bases/base_state1.png", b._position)
			elif b._vie >b.vie_depart/5 and b._vie <=b.vie_depart/2:
				self.ajouter_element("images/interface/bases/base_state2.png", b._position)
			else:
				self.ajouter_element("images/interface/bases/base_state3.png", b._position)
			self._joueur._carte[self.carte.objet_dans_case(b._position)] = "base"
		for pos in self._liste_rochers:
			self.ajouter_element("images/interface/rock2.png", pos)
			self._joueur._carte[self.carte.objet_dans_case(pos)] = "decor"
		# Affichage place de construction : A COMPLETER !
		for pc in self._places_construction:
			if self.carte[pc] != "tour":
				pos_x, pos_y = self.carte.positionner_objet(pc)
				self._joueur._carte[pc] = "place construction" # La case devient une place de construction
				self.ajouter_element("images/interface/place_construction.png", (pos_x, pos_y))
		for pos in self._liste_arbre:
			self.ajouter_element("images/interface/arbre2.png", pos)
			self._joueur._carte[self.carte.objet_dans_case(pos)] = "decor"
		for T in self.joueur.liste_tours:
			self.ajouter_element(self._listenoms_tours[T._id_tour], T._position)

	def affichage_armee(self, armee):
		for b in self._bases:
			for soldat in armee._liste_soldat:
				if soldat.vie != 0 and soldat._position != b._position:
					type_soldat = soldat._type_soldat
					anim_soldat = soldat._animation
					soldat.arriver_base(self._bases)
					self.ajouter_element(self._listenoms_soldats[type_soldat][soldat._direction][anim_soldat], soldat._position)
	def affichage_projectile(self,projectile):
		# im_projectile = pygame.image.load("images/tours/balle.png").convert_alpha()
		if projectile._position != projectile._arrivee:
			self.ajouter_element("images/tours/balle.png",projectile._position)

	def affichage_menu(self):
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
                if self.carte[pos_case]=="soldat":
                        self.ajouter_element("images/interface/bases/base_state1.png", (self.carte.largeur//4,self.carte.hauteur+50))
                        tmp = self.carte.objet_dans_case(pos)
			pos = self.carte.positionner_objet(tmp)
			for T in self._bases:
				if T._position == pos:
                                        text_base=font_menu.render("Base :"+str(T._vie),1,(255,255,255))
                                        self._fenetre.blit(text_base,(self.carte.largeur//4 + 50, self.carte.hauteur+50))
                        

	def affichage_menu2(self):
		""" Menu du haut de fenetre : Temps, Vie des bases, argent du joueur et son score """
		# Affichage du temps (Min:Sec)
		font_temps = pygame.font.Font(None, 36)
		temps = pygame.time.get_ticks()
		temps /= 1000
		secondes = temps%60
		minutes = temps//60
		text_temps = font_temps.render(str(minutes)+ " : "+ str(secondes), 1, (255, 255, 255))
		self._fenetre.blit(text_temps, (20,10))

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
