#!/usr/bin/python
#encoding: utf8

from affichage import *

def main():
	pygame.init()

	#Ouverture de la fenêtre Pygame
	C = Carte()
	J = Joueur(C)
	F = Affichage_fenetre(J)
	S = Soldat((0, C._hauteur/2))
	A = Armee([S], (19*C._largeur/20, 8*C._hauteur/16), J)
	continuer = 1
	#Chargement et collage du fond
	F.affichage_statique()
	F.genere_decor()
	F.affichage_decor()
	#Boucle infinie
	while continuer:
		pygame.display.flip()
		F.affichage_statique()
		F.affichage_pc()
		temps = pygame.time.get_ticks()
		F.affichage_armee(A)
		F.affichage_decor()
		F._joueur.affichage_portee(F._fenetre)
		F.affichage_tours()
		if (temps % 2 == 0):
			A.mouvement_troupe()
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus

			F._joueur.gestion_tour(event)
			F.affichage_tours()
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer = 0      #On arrête la boucle



if __name__ == '__main__':
    main()
