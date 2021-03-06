#!/usr/bin/python
#encoding: utf8

from test_scores import *
from affichage import *
import gtk, pygtk


def is_over(carte):
	for pos in carte._pos_bases:
		if carte[pos]._vie > 0:
			return False
	return True

def main():
	# RESOLUTION A RENTRER AUTREMENT
	window = gtk.Window()
	screen = window.get_screen()
	res_h = int(screen.get_height())
	res_l = int(screen.get_width())
	pygame.init()
	pygame.mixer.music.load("musique/musique_partie.wav")
	music_jeu_menu=pygame.mixer.Sound("musique/musique_menu.wav")
	music_game_over=pygame.mixer.Sound("musique/musique_gameover.wav")
	En_jeu = 0
	MJ = MenuJeu()
	tmp = 1
	music_jeu_menu.play()
	while(En_jeu != "Jouer" and tmp == 1):
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
		music_jeu_menu.fadeout(300)
		C = Carte("cartes_carte4", res_h, res_l)
		J = Joueur()
		F = Affichage_fenetre(J, C, res_l, res_h)
		S=[]
		C.initialiser_carte([0,10,0,20])
		A = Armee()
		tableau_projectile =[] # Tableau des projectiles
		continuer = 1
		clock = pygame.time.Clock()
		pygame.mixer.music.play()
		F.affichage_terrain(C)
		last_time = time.time()
		last_time_proj = time.time()

		compteur = 0
		gameover_bool = False
		etat_jeu = "play"
		while continuer:
			if is_over(C):
				pygame.mixer.music.fadeout(300)
				music_game_over.play()
				if not gameover_bool:
					gameover_bool = True
				  	#~ disparition
					for i in range(0,255,4):
						F._fenetre.fill((0,0,0))
				        pygame.display.flip()
					#~ apparition
					for i in range(255,0,-4):
					    F.ajouter_element("images/interface/"+\
						"GameOver2.png",(0,0), C)
					    F._fenetre.fill((i,i,i),special_flags=\
						BLEND_RGB_SUB)
					    pygame.display.flip()
					name =test_score(F._fenetre)
					score=J.score
					enter_new_score(name, score)
					#F.affichage_terrain()
					F.affiche_score(C, name, score)
					pygame.display.flip()
				else:
					pygame.time.Clock().tick(60)

					for event in pygame.event.get():
					    if event.type == QUIT:
					      continuer = 0
					    if event.type == KEYDOWN and event.key == K_ESCAPE:
					      pygame.display.toggle_fullscreen()
					tkey = pygame.key.get_pressed()
					if tkey[K_LALT] and tkey[K_F4]:
						continuer = 0
			else:
				compteur += 1
				rapidite = 60
				pygame.time.Clock().tick(rapidite)
				for event in pygame.event.get():
					if event.type != MOUSEMOTION:
						F.gestion_menu(C, event)
						if F._menu.interaction_menu_haut(C, event) \
						!= None :
							etat_jeu = F._menu.interaction_menu_haut(C,\
							 event)
					if event.type == QUIT:
						continuer = 0
					if event.type == KEYDOWN and event.key == K_ESCAPE:
						pygame.display.toggle_fullscreen()

				tkey = pygame.key.get_pressed()

				if tkey[K_LALT] and tkey[K_F4]:
					continuer = 0
				if etat_jeu == "accelerate":
					rapidite = 220

				F.affiche_all(C,A)
				C.actualise()
				J.miseajour_carte_cout_tours(C)
				F.gestion_menu(C)
				if etat_jeu == "play" or etat_jeu == "accelerate":

					#Mouvement des troupes
					A.actualisation(C,compteur)
					temps = pygame.time.get_ticks()

					#Gestion des projectiles
					i =0
					while(i<len(tableau_projectile)):
						F.ajouter_element("images/tours/balle.png", \
						tableau_projectile[i]._position, C)
						tableau_projectile[i].bouge(C)
						if(tableau_projectile[i].is_over()):
							del(tableau_projectile[i])
							i=i-1
						i=i+1

					#Gestion de l'attaque des tours
					for T in F._joueur._liste_tours:
						stock_attaque = (T.attaque(A, C))
						if(stock_attaque[0]):
							tableau_projectile.append(stock_attaque[1])
					argent, point = A.maj_troupe(C)
					F.joueur.actualise_valeurs((argent, point))
				pygame.display.flip()

if __name__ == '__main__':
    main()
