#!/usr/bin/python
#encoding: utf8

from joueur import *

class Affichage_fenetre:
	def __init__(self, joueur):
		self._listenoms_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._listenoms_soldats = [[["images/armee/boss/boss_bas.png", "images/armee/boss/boss_bas_pd.png", "images/armee/boss/boss_bas_pg.png"], "images/armee/boss/boss_gauche.png", "images/armee/boss/boss_haut.png", ["images/armee/boss/boss_droite.png", "images/armee/boss/boss_droite_pd.png", "images/armee/boss/boss_droite_pg.png"]]]
		self._joueur = joueur
		self._fenetre = pygame.display.set_mode((self._joueur._carte._largeur, self._joueur._carte._hauteur))
		self._nb_decor = [5, 5] # 10 Rochers, 5 Arbres
		self._liste_rochers = []
		self._liste_arbre = []
		self._bases = [Base(((self._joueur._carte._nb_cases_l-1)*self._joueur._carte._largeur/self._joueur._carte._nb_cases_l, self._joueur._carte._hauteur/self._joueur._carte._nb_cases_h*(self._joueur._carte._nb_cases_h//2)), self._joueur._carte)]
		self._places_construction = [(10,10), (15, 10), (3, 2)] # A MODIFIER

	@property
	def carte(self):
		return self._joueur._carte
	def joueur(self):
		return self._joueur
	def ajouter_element(self, nom_image, position):
		element = pygame.image.load(nom_image).convert_alpha()
		if "tour" in nom_image or "arbre" in nom_image:
			self._fenetre.blit(element, (position[0], position[1]-\
			self._joueur._carte._hauteur/self._joueur._carte._nb_cases_h))
		else:
			self._fenetre.blit(element, position)
	def affichage_pc(self):
		# Affichage place de construction : A COMPLETER !
		for pc in self._places_construction:
			if self._joueur._carte[pc] != "tour":
				pos_x, pos_y = self._joueur._carte.positionner_objet(pc)
				self._joueur._carte[pc] = "place construction" # La case devient une place de construction
				self.ajouter_element("images/interface/place_construction.png", (pos_x, pos_y))
	def affichage_statique(self):
		self.ajouter_element("images/interface/background2.jpg", (0, 0))
		# Affichage chemin :
		source = (0, self._joueur._carte._hauteur/2)
		tmp_case = source
		chemin = [source]
		self._joueur._carte[source] = "chemin"
		for position_chemin in chemin:
			self.ajouter_element("images/interface/route2.jpg", position_chemin)
			self._joueur._carte[self._joueur._carte.objet_dans_case(position_chemin)] = "chemin"
		# Affichage bases :
		for b in self._bases:
			self.ajouter_element("images/interface/base.png", b._position)
			self._joueur._carte[self._joueur._carte.objet_dans_case(b._position)] = "base"
	def genere_decor(self):
		for i in range(self._nb_decor[0]):
			tmp1, tmp2 = np.random.randint(self._joueur._carte._nb_cases_l-1), np.random.randint(self._joueur._carte._nb_cases_h-1)
			while self._joueur._carte[tmp1, tmp2] != "herbe":
				tmp1, tmp2 = np.random.randint(self._joueur._carte._nb_cases_l-1), np.random.randint(self._joueur._carte._nb_cases_h-1)
			pos_x, pos_y = self._joueur._carte.positionner_objet((tmp1,tmp2))
			self._joueur._carte[tmp1, tmp2] = "decor" # La case devient un decor
			self._liste_rochers.append((pos_x, pos_y))
		for i in range(self._nb_decor[1]):
			tmp1, tmp2 = np.random.randint(self._joueur._carte._nb_cases_l-1), np.random.randint(self._joueur._carte._nb_cases_h-1)
			while self._joueur._carte[tmp1, tmp2] != "herbe":
				tmp1, tmp2 = np.random.randint(self._joueur._carte._nb_cases_l-1), np.random.randint(self._joueur._carte._nb_cases_h-1)
			pos_x, pos_y = self._joueur._carte.positionner_objet((tmp1,tmp2))
			self._joueur._carte[tmp1, tmp2] = "decor" # La case devient un decor
			self._liste_arbre.append((pos_x, pos_y))

	def affichage_decor(self):
		for pos in self._liste_rochers:
			self.ajouter_element("images/interface/rock.png", pos)
			self._joueur._carte[self._joueur._carte.objet_dans_case(pos)] = "decor"
		for pos in self._liste_arbre:
			self.ajouter_element("images/interface/arbre.png", pos)
			self._joueur._carte[self._joueur._carte.objet_dans_case(pos)] = "decor"

	def affichage_tours(self):
		for T in self._joueur._liste_tours:
			self.ajouter_element(self._listenoms_tours[T._id_tour], T._position)

	def affichage_armee(self, armee):
		for b in self._bases:
			for soldat in armee._liste_soldat:
				type_soldat = soldat._type_soldat
				anim_soldat = soldat._animation
				self.ajouter_element(self._listenoms_soldats[type_soldat][soldat._direction][anim_soldat], soldat._position)
