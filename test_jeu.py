#!/usr/bin/python
#encoding: utf8

from affichage import *

def is_over(carte):
	for pos in carte._pos_bases:
		if carte._cases[pos[0]][pos[1]]._vie > 0:
			return False
	print("vies bases : ", [carte._cases[pos[0]][pos[1]]._vie for pos in carte._pos_bases])
	print("nb vagues : ", nb_vagues)
	return True


def duree_jeu():
	tmp = 1
	C = Carte("cartes_carte3")
	J = Joueur(C)
	S=[]
	C.initialiser_carte([0,10,0,20])
	A = Armee()
	nb_vagues = 1
	continuer = 1

	compteur = 0
	liste_pos_pc = []
	for x in range(0,C.nb_cases_l):
		for y in range(0,C.nb_cases_h):
			if C.get_type_case((x,y))=="place_construction":
				liste_pos_pc.append((x,y))


	#Boucle infinie
	while continuer:
		compteur += 1 # A modifier pour une vitesse x2

		# L'IA Joue :
		if (len(liste_pos_pc)!=0):
			J.construire_tour(1,liste_pos_pc[0])
			del liste_pos_pc[0]
		else:
			for T in J.liste_tours:
				if (J.ameliorer_tour(T)):
					break


		C.actualise()
		i =0
		#Gestion des projectiles

		#Mouvement des troupes
		if (compteur%2 == 0):
			A.mouvement_troupe(C)
			#last_time = time.time()
		#temps = pygame.time.get_ticks()

		if (compteur%10 == 0) and [C.get_base(i)._vie for i in range(len(C._pos_bases))] != [0]*len(C._pos_bases):
			A.actualise_vague(C)

		#Gestion de l'attaque des tours
		if (compteur%2 == 0):
			for T in F._joueur._liste_tours:
				stock_attaque = (T.attaque(A, C))

		F.joueur.actualise_valeurs( A.maj_troupe(C))
		pygame.display.flip()
			#last_time = time.time()

duree_jeu()
