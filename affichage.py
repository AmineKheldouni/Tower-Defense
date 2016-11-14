#!/usr/bin/python
#encoding: utf8

from joueur import *

class Affichage_fenetre:
	def __init__(self, carte, joueur):
		self._liste_tours = ["images/tours/tour1.png", "images/tours/tour2.png"]
		self._tableau_type_armee = [1] # la position i de ce tableau renvoie le nombre de soldats de type i dans l'armee qui passe actuellement
		self._liste_soldats = [["images/armee/boss/boss_bas.png", "images/armee/boss/boss_gauche.png", "images/armee/boss/boss_haut.png", "images/armee/boss/boss_droite.png"]]
		self._carte = carte
		self._fenetre = pygame.display.set_mode((self._carte._largeur, self._carte._hauteur))
		self._nb_decor = [10, 15] # 10 Rochers, 5 Arbres
		self._liste_rochers = []
		self._liste_arbre = []
		self._joueur = joueur
		self._bases = [Base(((self._carte._nb_cases_l-1)*self._carte._largeur/self._carte._nb_cases_l, self._carte._hauteur/self._carte._nb_cases_h*(self._carte._nb_cases_h//2)), self._carte)]
		self._places_construction = [(10,10), (15, 10), (3, 2)]

	def ajouter_element(self, nom_image, position):
		element = pygame.image.load(nom_image).convert_alpha()
		if "tour" in nom_image or "arbre" in nom_image:
			self._fenetre.blit(element, (position[0], position[1]-\
			self._carte._hauteur/self._carte._nb_cases_h))
		else:
			self._fenetre.blit(element, position)

	def affichage_statique(self):
		self.ajouter_element("images/interface/background2.jpg", (0, 0))
		# Affichage place de construction : A COMPLETER !
		for pc in self._places_construction:
			pos_x = pc[0] * self._carte._largeur/self._carte._nb_cases_l
			pos_y = pc[1] * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[pc] = 2 # La case devient une place de construction
			self.ajouter_element("images/interface/place_construction.png", (pos_x, pos_y))
		# Affichage chemin :
		source = (0, self._carte._hauteur/2)
		tmp_case = source
		chemin = [source]
		self._carte[source] = 1
		"""pas_l = self._carte._largeur/self._carte._nb_cases_l
		pas_h = self._carte._hauteur/self._carte._nb_cases_h
		cases_voisines = [(-pas_l,0), (pas_l, 0), (0, -pas_h), (0, pas_h)]
		for b in self._bases:
			dist_base = m.sqrt((tmp_case[0]-b._position[0])**2+(tmp_case[1]-b._position[1])**2)
			while tmp_case != b.position:
				meilleur_voisin = tmp_case
				min_dist = dist_base
				for voisin in cases_voisines:
					tmp_case2 = tmp_case[0]+voisin[0], tmp_case[1]+voisin[1]
					dist_base2 = m.sqrt((tmp_case2[0]-b._position[0])*\
					(tmp_case2[0]-b._position[0])+(tmp_case2[1]-b._position[1])\
					*(tmp_case2[1]-b._position[1]))
					if self._carte[tmp_case2] == 5:
						if dist_base2 <= dist_base:
							meilleur_voisin = tmp_case2
				min_dist = dist_base2
				self._carte[meilleur_voisin] = 1
				chemin.append(meilleur_voisin)"""

		for position_chemin in chemin:
			self.ajouter_element("images/interface/route.jpg", position_chemin)


			# Affichage bases :
			for b in self._bases:
				self.ajouter_element("images/interface/base.png", b._position)

	def genere_decor(self):
		for i in range(self._nb_decor[0]):
			tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			while self._carte[tmp1, tmp2] != 5:
				tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			pos_x = tmp1 * self._carte._largeur/self._carte._nb_cases_l
			pos_y = tmp2 * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[tmp1, tmp2] = 1 # La case devient un decor
			self._liste_rochers.append((pos_x, pos_y))
		for i in range(self._nb_decor[1]):
			tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			while self._carte[tmp1, tmp2] != 5:
				tmp1, tmp2 = np.random.randint(self._carte._nb_cases_l-1), np.random.randint(self._carte._nb_cases_h-1)
			pos_x = tmp1 * self._carte._largeur/self._carte._nb_cases_l
			pos_y = tmp2 * self._carte._hauteur/self._carte._nb_cases_h
			self._carte[tmp1, tmp2] = 1 # La case devient un decor
			self._liste_arbre.append((pos_x, pos_y))

	def affichage_decor(self):
		for pos in self._liste_rochers:
			self.ajouter_element("images/interface/rock.png", pos)
		for pos in self._liste_arbre:
			self.ajouter_element("images/interface/arbre.png", pos)

	def affichage_tours(self):
		for T in self._joueur._liste_tours:
			self.ajouter_element(self._liste_tours[T._id_tour], T._position)

	def affichage_armee(self, armee):
		for b in self._bases:
			for soldat in armee._liste_soldat:
				type_soldat = soldat._type_soldat
				self.ajouter_element(self._liste_soldats[type_soldat][soldat._direction], soldat._position)
