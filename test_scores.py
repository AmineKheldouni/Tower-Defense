#!/usr/bin/python
#encoding: utf8

from affichage import *

def main():
	pygame.init()
	F = pygame.display.set_mode((640, 360), pygame.RESIZABLE)	# A MODIFIER
	continuer = 1
	ask = str("Entrez votre pseudo ")
	font =  pygame.font.Font("Blacksword.otf",65)
	font2 =  pygame.font.Font("Blacksword.otf",50)
	txt_ask = font.render(ask, 1, (255, 255, 255))
	pseudo = ""
	while (continuer == 1):
		F.fill((0,0,0))
		F.blit(txt_ask, (60,40))
		txt_pseudo = font2.render(pseudo, 1, (200, 200, 200))
		F.blit(txt_pseudo, (150, 200))
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				pygame.display.toggle_fullscreen()
			if event.type == KEYDOWN and event.key == K_RETURN:
				continuer = 0
			if event.type == KEYDOWN and (event.key != K_BACKSPACE) and event.key != K_RETURN:
				s = pygame.key.name(event.key)
				if len(s) == 1:
					pseudo += s
			if event.type == KEYDOWN and (event.key == K_BACKSPACE):
				pseudo = pseudo[0:len(pseudo)-1]
		pygame.display.flip()

	print("Votre pseudo : ", pseudo)
if __name__ == '__main__':
    main()
