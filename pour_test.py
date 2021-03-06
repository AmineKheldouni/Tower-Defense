#!/usr/bin/python
#encoding: utf8

from affichage import *

def is_over(carte):
	for pos in carte._pos_bases:
		if carte._cases[pos[0]][pos[1]]._vie > 0:
			return False
	return True

def main():
	pygame.init()
	En_jeu = 0
	MJ = MenuJeu()
	tmp = 1
	while(En_jeu == 0 and tmp == 1):
		MJ.maj_image()
		for event in pygame.event.get():
			if event.type == QUIT:
				tmp = 0
			if event.type == KEYDOWN and event.key == K_ESCAPE:
			  pygame.display.toggle_fullscreen()
		tkey = pygame.key.get_pressed()
		if tkey[K_LALT] and tkey[K_F4]:
			tmp = 0
		MJ.maj_menu(event)
		En_jeu = MJ._etat
		if En_jeu == "Quit":
			print("Sortie du jeu")
			return 0
	if En_jeu == "Jouer":
		#Ouverture de la fenêtre Pygame
		C = Carte("cartes_carte4")
		C.initialiser_carte([5,4,3,2])
		J = Joueur(C)
		F = Affichage_fenetre(J)
		A = Armee()
		tableau_projectile =[] # Tableau des projectiles
		continuer = 1
		clock = pygame.time.Clock()
		FPS = 30.
		#font_cambria = pygame.font.SysFont('Cambria', 24)
		#fps_label = font_cambria.render('FPS : {}'.format(clock.get_fps()), True, (255, 255, 255))
		#fps_rect = fps_label.get_rect(bottomright = (C.largeur, C.hauteur))
		#pygame.time.set_timer()
		#Chargement et collage du fond
		F.affichage_terrain()
		last_time = time.time()
		last_time_proj = time.time()
		#F.affichage_menu(A)
		compteur = 0
		gameover_bool = False
		#Boucle infinie
		while continuer:
			if is_over(C):
				if not gameover_bool:
					gameover_bool = True
				  	#~ disparition
					for i in range(0,255,4):
						F._fenetre.fill((0,0,0))
				        pygame.display.flip()
					#~ apparition
					for i in range(255,0,-4):
					    F.ajouter_element("images/interface/GameOver2.png",(0,0))
					    F._fenetre.fill((i,i,i),special_flags=BLEND_RGB_SUB)
					    pygame.display.flip()
				else:
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
					#F._joueur.gestion_tour(event)
					F.gestion_menu(event)
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
				#Graphic
				F.affiche_all(C,A)
				#F._fenetre.blit(fps_label, fps_rect)
				#if True:
					# if((time.time()-last_time_proj)> 0.05):
					#last_time_proj=time.time()
					# Gestion de l'avancée des projectiles
					#La boucle while sert à gérer les destructions pour éviter les dépassement d'indice
				# Gestion des objets de la carte
				C.actualise()
				i =0
				#Gestion des projectiles
				while(i<len(tableau_projectile)):
					F.ajouter_element("images/tours/balle.png",tableau_projectile[i]._position)
					tableau_projectile[i].bouge()
					if(tableau_projectile[i].is_over()):
						del(tableau_projectile[i])
						i=i-1
					i=i+1
				#Mouvement des troupes
				if (compteur%2 == 0):
					A.mouvement_troupe(C)
					#last_time = time.time()
				#temps = pygame.time.get_ticks()

				if (compteur%10 == 0) and [C.get_base(i)._vie for i in range(len(C._pos_bases))] != [0]*len(C._pos_bases):
					A.actualise_vague(C)
					temps = pygame.time.get_ticks()

				#Gestion de l'attaque des tours
				if (compteur%2 == 0):
					for T in F._joueur._liste_tours:
						stock_attaque = (T.attaque(A, F, F._joueur.carte))
						if(stock_attaque[0]):
							tableau_projectile.append(stock_attaque[1])
				F.joueur.actualise_valeurs( A.maj_troupe(C))
				pygame.display.flip()
					#last_time = time.time()

if __name__ == '__main__':
    main()
