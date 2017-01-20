#!/usr/bin/python
#encoding: utf8

from affichage import *

def is_over(carte):
	for pos in carte._pos_bases:
		if carte._cases[pos[0]][pos[1]]._vie > 0:
			return False
	return True


def duree_jeu():
	tmp = 1
	C = Carte("cartes_carte3")
	J = Joueur(C)
	S=[]
	J._carte.initialiser_carte([0,10,0,20])
	A = Armee()
	nb_vagues = 1
	continuer = 1

	compteur = 0
	nb_amelioree = 0
	liste_pos_pc = []
	for x in range(0,J.carte.nb_cases_l):
		for y in range(0,J.carte.nb_cases_h):
			if J.carte.get_type_case((x,y))=="place_construction":
				liste_pos_pc.append((x,y))

	print("Argent joueur t=0 : ", J._argent)
	#Boucle infinie
	while (is_over(J.carte)==False):
		compteur += 1 # A modifier pour une vitesse x2

		if (compteur%100 == 0):
			print("Nombre tours :", len(J._liste_tours))
			print("Nombre PC : ", len(liste_pos_pc))
			print("Nombre de tours ameliorees : ", nb_amelioree)
			print("Argent joueur : ", J._argent)
			print("vies bases : ", [J._carte._cases[pos[0]][pos[1]]._vie for pos in J._carte._pos_bases])
			#print("nb vagues : ", nb_vagues)

		# L'IA Joue :
		if (len(liste_pos_pc)!=0):
			if (J.construire_tour(1,liste_pos_pc[0])):
				del liste_pos_pc[0]
		else:
			for T in J.liste_tours:
				if T._munitions == 0:
					if (J.reparer_tour(T)):
						break

				else:
					if (J.ameliorer_tour(T)):
						nb_amelioree += 1
						break


		J.carte.actualise()
		i =0
		#Gestion des projectiles

		#Mouvement des troupes
		if (compteur%2 == 0):
			A.mouvement_troupe(C)
			#last_time = time.time()
		#temps = pygame.time.get_ticks()

		if (compteur%100 == 0) and [J.carte.get_base(i)._vie for i in range(len(J.carte._pos_bases))] != [0]*len(J.carte._pos_bases):
			A.actualise_vague(J.carte)
			nb_vagues += 1
		#Gestion de l'attaque des tours
		if (compteur%2 == 0):
			for T in J.liste_tours:
				stock_attaque = (T.attaque(A, J.carte))

		J.actualise_valeurs(A.maj_troupe(J.carte))
	print("vies bases : ", [J._carte._cases[pos[0]][pos[1]]._vie for pos in J._carte._pos_bases])
	
duree_jeu()
print("fin test")
