#!/usr/bin/python
#encoding: utf8

from affichage import *


def main():
	pygame.init()
	clock = pygame.time.Clock()
	#Ouverture de la fenêtre Pygame
	C = Carte()
	J = Joueur(C)
	F = Affichage_fenetre(J)
	pos_source = (C.nb_cases_l//5, C.nb_cases_h-1)
	pos_source = C.positionner_objet(pos_source)
	pos_source2 = (C.nb_cases_l//5, C.nb_cases_h-2)
	pos_source2 = C.positionner_objet(pos_source2)
	pos_source3 = (C.nb_cases_l//5, C.nb_cases_h-3)
	pos_source3 = C.positionner_objet(pos_source3)
	S = Soldat(pos_source, F._joueur, (C.nb_cases_l//2, 0))
	S2 = Soldat(pos_source2, F._joueur, (C.nb_cases_l//2, 0))
	S3 = Soldat(pos_source3, F._joueur, (C.nb_cases_l//2, 0))
	A = Armee([S, S2, S3], F._joueur)
	tableau_projectile =[] # Tableau des projectiles
	continuer = 1
	#Chargement et collage du fond
	F.affichage_terrain()
	F.formation_chemin()
	F.affichage_chemin()
	F.affichage_statique()
	F.genere_decor()
	F.affichage_chemin()
	F.affichage_statique()
	last_time = time.time()
	last_time_proj = time.time();
	#Boucle infinie
	while continuer:
		pygame.display.flip()
		F.affichage_terrain()
		F.affichage_chemin()
		temps = pygame.time.get_ticks()
		F._joueur.affichage_portee(F._fenetre)
		F.affichage_statique()
		F.affichage_armee(A)
		F.affichage_statique()
		if True:
		# if((time.time()-last_time_proj)> 0.05):
			last_time_proj=time.time()
			# Gestion de l'avancée des projectiles
			#La boucle while sert à gérer les destructions pour éviter les dépassement d'indice
			i =0;
			while(i<len(tableau_projectile)):
				F.ajouter_element("images/tours/balle.png",tableau_projectile[i]._position)
				tableau_projectile[i].bouge()
				if(tableau_projectile[i].is_over()):
					del(tableau_projectile[i])
					i=i-1
				i=i+1
		if (time.time()-last_time > 0.2):
			A.mouvement_troupe(F._bases)
			last_time = time.time()
		if (temps % 10 == 0):
			S = Soldat(pos_source, F._joueur, (C.nb_cases_l//2, 0))
			S2 = Soldat(pos_source2, F._joueur, (C.nb_cases_l//2, 0))
			A._liste_soldat.append(S)
			A._liste_soldat.append(S2)
		temps = pygame.time.get_ticks()

		#Gestion de l'attaque des tours
		if (temps % 4 == 0):
			for T in F._joueur._liste_tours:
				stock_attaque = (T.attaque(A, F))
				if(stock_attaque[0]):
					tableau_projectile.append(stock_attaque[1])
			last_time = time.time()
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			F._joueur.gestion_tour(event)
			F.affichage_statique()
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer = 0      #On arrête la boucle



if __name__ == '__main__':
    main()
