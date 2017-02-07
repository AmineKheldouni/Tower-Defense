#!/usr/bin/python
#encoding: utf8

from gestion_fenetre import *
from objet_actif import *
from vague import *

import random
# AJOUTER LA CLASSE ARMEE ET SOLDAT PUIS LA CLASSE PROJECTILE
class Soldat(Objet_Actif):
	def __init__(self, source, id_soldat=1):
		super(Soldat,self).__init__(source.position,"soldat",id_soldat)
		""" Les champs position et vitesse sont deux vecteurs de composantes x et y
	    valeur_soldat correspond à la valeur que le joueur obtient s'il l'élimine"""
		self._type_soldat   = ExtractIntFromFile("data_armee.csv",id_soldat,0)
		self._vie           = ExtractIntFromFile("data_armee.csv",id_soldat,2)
		self._vitesse       = ExtractIntFromFile("data_armee.csv",id_soldat,4)
		self._degat         = ExtractIntFromFile("data_armee.csv",id_soldat,5)
		self._valeur_soldat = ExtractIntFromFile("data_armee.csv",id_soldat,6)	# Score du joueur en tuant ce type de soldat
		self._argent_soldat = ExtractIntFromFile("data_armee.csv",id_soldat,7)
		self._graphic       = ExtractStrFromFile("data_armee.csv",id_soldat,8)

		self._position = source.position
		self._ancienne_position = self._position
		self._is_dead = False
		self._direction = source.get_a_direction() # 0 : bas, 1 : gauche, 2 : haut, 3 : droite
		self._animation = 0 # 0 : statique 1 : pied droit 2 : pied gauche
		self._pas = 0 #position dans la case
		self._value_case = 100 #valeur d'une case
		self._voisins = [(0, 1), (-1,0), (0, -1), (1, 0)]

	def est_mort(self):
		return self._est_mort or self._vie ==0

	@property
	def vie(self):
		return self._vie

	@property
	def vitesse(self):
	    return self._vitesse

	@property
	def position(self):
	    return self._position

	@property
	def degat(self):
	    return self._degat

	@property
	def valeur_soldat(self):
	    return self._valeur_soldat
	@property
	def pas(self):
		return self._pas

	def deplacement_soldat(self,carte):
		self._pas = self._pas + self._vitesse
		self.anime()
		if(self._pas >= self._value_case):
			self._pas-=self._value_case
			self.maj_direction(carte)

	def arriver_base(self,carte):
		pos_case = self._position
		if carte.get_type_case(pos_case) == "base":
			carte[pos_case].dommage(self._degat)
			return True
		return False

	def maj_direction(self,carte):
		pos_case = self._position
		liste_voisins = []
		liste_direction = []
		for i,voisin in enumerate(self._voisins):
			tmp_a, tmp_b = (pos_case[0]+voisin[0]), (pos_case[1]+voisin[1])
			case_voisin = (tmp_a, tmp_b)
			if(case_voisin in carte):
				if (carte.est_case_chemin(case_voisin,i)) and case_voisin != (self._position) and case_voisin != (self._ancienne_position):
					liste_voisins.append(case_voisin)
					liste_direction.append(i)
		if(len(liste_voisins)==1):
			chosen_path = 0
		if(len(liste_voisins)>1):
			chosen_path  = self.choix_chemin_pondere(liste_voisins, carte)
		if len(liste_voisins)>0:
			self._ancienne_position = self._position
			self._direction = liste_direction[chosen_path]
			self._position= liste_voisins[chosen_path]
		if(len(liste_voisins)==0):
			self._position = self._ancienne_position
			self._direction = (self._direction+2)%4

	def choix_chemin_deterministe(self, liste_voisin, carte):
		ind = 0
		cout_min = carte.get_cout_chemin(liste_voisin[0])
		for i in range(len(liste_voisin)):
			cout = carte.get_cout_chemin(liste_voisin[i])
			if(cout_min>cout):
				ind = i
				cout_min = cout
		return ind

	def pondere_inverse(self, valeur):
		return 100/(float(valeur*valeur))

	def choix_chemin_pondere(self, liste_voisin, carte):
		ind = 0
		coef = 0
		cout = [self.pondere_inverse(carte.get_cout_chemin(liste_voisin[0]))]*len(liste_voisin)
		for i in range(1,len(liste_voisin)):
			cout[i]= cout[i-1]+self.pondere_inverse(carte.get_cout_chemin(liste_voisin[i]))
		value_random = random.uniform(0,cout[len(cout)-1])
		while(value_random>cout[ind]):
			ind = ind+1
			assert(ind<len(cout))
		return ind


	def maj_direction4(self,carte):
		pos_case = self._position
		numero_base=self._numero_base_visee
		chemin=carte._carte_des_chemins[numero_base][pos_case[0]][pos_case[1]]
		print("chemin")
		print(chemin)
		print("soldat maj")
		choix_voisin = None
		liste_voisinins = []
		self.liste_vitesses = []
		self._liste_voisins_vitesses_cout=[]
		case_suivante=chemin[-2]
		pos_x_suivante=case_suivante[0]
		pos_y_suivante=case_suivante[1]
		case_voisin=(pos_x_suivante,pos_y_suivante)

		voisin_x=pos_x_suivante-pos_case[0]
		voisin_y=pos_y_suivante-pos_case[1]
		voisin_vitesse=(voisin_x,voisin_y)

		choix_voisin=case_voisin,voisin_vitesse

		if choix_voisin != None:
			self._direction = self._voisins.index(choix_voisin[1])
			self._ancienne_position = self._position
			self._position= choix_voisin[0]

	def dir_to_graph(self):
		dir_vect=["_bas","_gauche","_haut","_droite"]
		dir_anim=["","_pd","_pg"]
		return dir_vect[self._direction]+dir_anim[self._animation]

	def anime(self):
		self._animation += 1
		if self._animation == 3:
			self._animation = 0

	def actualisation(self):
		self.actualise_etat()


class Armee(Vague):
	"""
	Vecteur contenant l'ensemble des soldats
	"""
	def __init__(self, id_vague=1):
		super(Armee,self).__init__()
		self._liste_soldat = []
		self._time_before_wave = 20
		self._time_before_soldier = 10

	def mouvement_troupe(self,carte):
		soldats_arrives = []
		for i in range(len(self._liste_soldat)):
			soldat = self._liste_soldat[i]
			soldat.actualisation()
			soldat.deplacement_soldat(carte)

	def nb_soldats(self):
		return len(self._liste_soldat)

	def ajout_soldat(self, pos, id_soldat):
		self._liste_soldat.append(Soldat(pos,id_soldat))

	def actualise_vague(self, carte):
		if(self.nb_soldats() < self._nb_max_ennemis_sur_carte):
			for i in range(len(carte._pos_sources)):
				indice = self.renvoie_soldat()
				if(indice>0):
					self.ajout_soldat(carte.get_source(i), indice)

	def maj_troupe(self,carte):
		liste_morts = []
		argent = 0
		point  = 0
		idx = 0
		while idx < len(self._liste_soldat):
			soldat = self._liste_soldat[idx]
			if soldat.est_mort():
				argent+=self._liste_soldat[idx]._argent_soldat
				point +=self._liste_soldat[idx]._valeur_soldat
				del(self._liste_soldat[idx])
				idx = idx -1
			elif(soldat.arriver_base(carte)):
				del(self._liste_soldat[idx])
				idx = idx -1
			idx = idx+1
		return(argent, point)

	def actualisation(self, carte, compteur):
		if(not self.armee_is_over()):
			self.mouvement_troupe(carte)
			if(compteur%self._time_before_soldier == 0):
				self.actualise_vague(carte)
		else:
			if(self._time_before_wave == 0):
				self.new_wave()
				self._time_before_wave = 50
			else:
				self._time_before_wave -=1


	def armee_is_over(self):
		return self.wave_is_over() and self.nb_soldats()==0
