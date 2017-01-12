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
    if True:
        #Ouverture de la fenêtre Pygame
        C = Carte("cartes_carte2")
        C.actualise_cout_chemin()


if __name__ == '__main__':
    main()
