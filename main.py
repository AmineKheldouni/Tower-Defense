#!/usr/bin/python
#encoding: utf8

from affichage import *
def is_over(liste_bases):
	for x in liste_bases:
		if x._vie > 0:
			return False
	return True

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
	pos_source3 = (C.nb_cases_l//5, C.nb_cases_h-3)
	pos_source3 = C.positionner_objet(pos_source3)
	S = Soldat(pos_source, F._joueur, (C.nb_cases_l//2, 0))
	S2 = Soldat(pos_source2, F._joueur, (C.nb_cases_l//2, 0))
	S3 = Soldat(pos_source3, F._joueur, (C.nb_cases_l//2, 0))
	A = Armee([S, S2, S3], F._joueur)
	tableau_projectile =[] # Tableau des projectiles
	continuer = 1

	clock = pygame.time.Clock()
	FPS = 120
	#font_cambria = pygame.font.SysFont('Cambria', 24)
	#fps_label = font_cambria.render('FPS : {}'.format(clock.get_fps()), True, (255, 255, 255))
	#fps_rect = fps_label.get_rect(bottomright = (C.largeur, C.hauteur))
	#pygame.time.set_timer()
	#Chargement et collage du fond
	F.affichage_terrain()
	F.formation_chemin()
	F.affichage_statique()
	F.genere_decor()
	F.affichage_chemin()
	F.affichage_statique()
	last_time = time.time()
	last_time_proj = time.time()
	#F.affichage_menu(A)
	compteur = 0
	#Boucle infinie
	while continuer:
		if is_over(F._bases):
			pygame.time.wait(2000)
			F._fenetre.fill((0,0,0))
			game_over = F.ajouter_element("images/interface/GameOver.png", (0,0))
			pygame.display.flip()
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = 0      #On arrête la boucle
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					pygame.display.toggle_fullscreen()
			tkey = pygame.key.get_pressed()
			if tkey[K_LALT] and tkey[K_F4]:
				continuer = 0
		else:
			compteur += 1 # A modifier pour une vitesse x2
			#clock.tick(FPS)
			#time.sleep(0.02)

			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				F._joueur.gestion_tour(event)
				F.affichage_statique()
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = 0      #On arrête la boucle
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					pygame.display.toggle_fullscreen()
			tkey = pygame.key.get_pressed()

			if tkey[K_LALT] and tkey[K_F4]:
				continuer = 0
			#dt = clock.tick() / 1000
			dt=1
			# Vider la fenêtre

			F.affichage_terrain()
			F.affichage_carte()
			F.affichage_statique()
			F.affichage_armee(A)
			F.affichage_statique()
			F.affichage_menu(A)

			F.gestion_menu()
			F.affichage_portee()
			#F._fenetre.blit(fps_label, fps_rect)
			#if True:
				# if((time.time()-last_time_proj)> 0.05):
				#last_time_proj=time.time()
				# Gestion de l'avancée des projectiles
				#La boucle while sert à gérer les destructions pour éviter les dépassement d'indice
			i =0
			while(i<len(tableau_projectile)):
				F.ajouter_element("images/tours/balle.png",tableau_projectile[i]._position)
				tableau_projectile[i].bouge()
				if(tableau_projectile[i].is_over()):
					if tableau_projectile[i]._soldat_cible._vie == 0:
						tableau_projectile[i]._soldat_cible._is_dead = True
					del(tableau_projectile[i])
					i=i-1
				i=i+1
			pygame.display.flip()
			if (compteur%2 == 0):
				A.mouvement_troupe(F._bases, dt)
				for projectile in tableau_projectile:
					projectile.set_arrivee(projectile._soldat_cible._position)
				#last_time = time.time()
			#temps = pygame.time.get_ticks()
			if (compteur%2 == 0):
				if (compteur>5):
					F._joueur.gain(compteur//5)
			if (compteur%10 == 0) and [F._bases[i]._vie for i in range(len(F._bases))] != [0]*len(F._bases):
				S = Soldat(pos_source, F._joueur, (C.nb_cases_l//2, 0))
				S2 = Soldat(pos_source2, F._joueur, (C.nb_cases_l//2, 0))
				A._liste_soldat.append(S)
				A._liste_soldat.append(S2)
			#temps = pygame.time.get_ticks()

			#Gestion de l'attaque des tours
			if (compteur%5 == 0):
				for T in F._joueur._liste_tours:
					stock_attaque = (T.attaque(A, F))
					if(stock_attaque[0]):
						tableau_projectile.append(stock_attaque[1])
				#last_time = time.time()


if __name__ == '__main__':
    main()
