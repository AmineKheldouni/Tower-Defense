#!/usr/bin/python
#encoding: utf8

from affichage import *

def main():
	pygame.init()

	#Ouverture de la fenêtre Pygame
	C = Carte()
	J = Joueur(C)
	F = Affichage_fenetre(J)
	pos_source = (C.nb_cases_l//5, C.nb_cases_h-1)
	pos_source = C.positionner_objet(pos_source)
	pos_source2 = (C.nb_cases_l//5, C.nb_cases_h-2)
	pos_source2 = C.positionner_objet(pos_source2)
	S = Soldat(pos_source, F._joueur, (C.nb_cases_l//2, 0))
	S2 = Soldat(pos_source2, F._joueur, (C.nb_cases_l//2, 0))
	A = Armee([S, S2], F._joueur)
	continuer = 1
	#Chargement et collage du fond
	F.affichage_terrain()
	F.formation_chemin()
	F.affichage_chemin()
	F.affichage_statique()
	F.genere_decor()
	F.affichage_chemin()
	F.affichage_statique()
	#Boucle infinie
	while continuer:
		pygame.display.flip()
		F.affichage_terrain()
		F.affichage_chemin()
		F.affichage_statique()
		temps = pygame.time.get_ticks()
		F._joueur.affichage_portee(F._fenetre)
		F.affichage_armee(A)
		F.affichage_statique()
		for T in F._joueur._liste_tours:
			T.attaque(A)
		if (temps % 2 == 0):
			A.mouvement_troupe()
		if (temps % 10 == 0):
			S = Soldat(pos_source, F._joueur, (C.nb_cases_l//2, 0))
			S2 = Soldat(pos_source2, F._joueur, (C.nb_cases_l//2, 0))
			A._liste_soldat.append(S)
			A._liste_soldat.append(S2)
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			F._joueur.gestion_tour(event)
			F.affichage_statique()
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer = 0      #On arrête la boucle



if __name__ == '__main__':
    main()
