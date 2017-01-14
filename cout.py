#!/usr/bin/python
#encoding: utf8

from scvuser import *

class Carte_Cout():
    """docstring for Carte_Cout."""
    def __init__(self,longueur, largeur, id_carte):
        cout_case=[[ 1 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
        cout_chemin=[[ 1 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]

#fonction récursive utilisée pour créer la carte des couts
def miseajour_carte_couts_aux(numero_base,matrice_a_remplir,position_a_remplir,cout,nb_cases_l,nb_cases_h,fonction_de_chemin):
	if((matrice_a_remplir[numero_base][position_a_remplir[0]][position_a_remplir[1]]==-1)):
		matrice_a_remplir[numero_base][position_a_remplir[0]][position_a_remplir[1]]=cout
		for i in [0,1,3]:
			direction=i
			position_x=position_a_remplir[0]
			position_y = position_a_remplir[1]
			position_x+= liste_des_voisins_possible[i][0]
			position_y+= liste_des_voisins_possible[i][1]
			position_aux=(position_x,position_y)
			if((position_aux[0]>=0) and (position_aux[0]<nb_cases_l) and (position_aux[1]>=0) and (position_aux[1]<nb_cases_h) and (fonction_de_chemin(position_aux,direction)) ):
				print("fuck")
				miseajour_carte_couts_aux(numero_base,matrice_a_remplir,position_aux,cout+1,nb_cases_l,nb_cases_h,fonction_de_chemin)
				print("da fuck")

def cout_dun_chemin(liste_chemin):
	res=0
	for i in range(len(liste_chemin)):
		res=res+liste_chemin[i][2]
	return res

#liste_chemin contient des triplets reliant la base à la dernière position du chemin
def miseajour_carte_chemin_aux(numero_base,matrice_a_remplir_chemin,matrice_de_couts,position_a_remplir,liste_chemin,nb_cases_l,nb_cases_h,fonction_chemin):
	coord_x=position_a_remplir[0]
	coord_y=position_a_remplir[1]
	print("utilisation fonction mise a jour")
	print("base est reconnue chemin?")
	print(fonction_chemin(position_a_remplir))
	if(liste_chemin==[]):
		print("on rentre dans la mise a jour d'une base")
		case=(coord_x,coord_y,matrice_de_couts[numero_base][coord_x][coord_y])
		matrice_a_remplir_chemin[numero_base][coord_x][coord_y]==[case]
		liste_chemin=[case]
		for i in range(4):
			pos_x=coord_x
			pos_y=coord_y
			pos_x+= liste_des_voisins_possible[i][0]
			pos_y+= liste_des_voisins_possible[i][1]
			position_aux=(pos_x,pos_y)
			liste_intermediaire=list(liste_chemin)
			miseajour_carte_chemin_aux(numero_base,matrice_a_remplir_chemin,matrice_de_couts,position_aux,liste_intermediaire,nb_cases_l,nb_cases_h,fonction_chemin)


	else:
		print("liste des chemins")
		print(liste_chemin)
		derniere_position_x=liste_chemin[-1][0]
		derniere_position_y=liste_chemin[-1][1]

		direction_x=derniere_position_x-coord_x
		direction_y=derniere_position_y-coord_y

		direction=dictionnaire_direction[(direction_x,direction_y)]

		if((coord_x>=0) and (coord_x<nb_cases_l) and (coord_y>=0) and (coord_y<nb_cases_h) and fonction_chemin(position_a_remplir,direction)):
			print("on rentre dans la mise a jour d'une base")
			if(matrice_a_remplir_chemin[numero_base][coord_x][coord_y]==[]):
				liste_nouveau_chemin=list(liste_chemin)
				case=(coord_x,coord_y,matrice_de_couts[numero_base][coord_x][coord_y])
				liste_nouveau_chemin.append(case)
				matrice_a_remplir_chemin[numero_base][coord_x][coord_y]=list(liste_nouveau_chemin)
				print("mise a jour connard?")
				print(matrice_a_remplir_chemin[numero_base][coord_x][coord_y])
				for i in range(4):
					pos_x=coord_x
					pos_y=coord_y
					pos_x+= liste_des_voisins_possible[i][0]
					pos_y+= liste_des_voisins_possible[i][1]
					position_aux=(pos_x,pos_y)
					liste_voisins=list(liste_nouveau_chemin)
					miseajour_carte_chemin_aux(numero_base,matrice_a_remplir_chemin,matrice_de_couts,position_aux,liste_voisins,nb_cases_l,nb_cases_h,fonction_chemin)

				else:

					cout_ancien_chemin=cout_dun_chemin(matrice_a_remplir_chemin[numero_base][coord_x][coord_y])
					cout_nouveau_chemin=cout_dun_chemin(liste_chemin)+matrice_de_couts[numero_base][coord_x][coord_y]

					if(cout_nouveau_chemin<cout_ancien_chemin):
						liste_nouveau_chemin=list(liste_chemin)
						case=(coord_x,coord_y,matrice_de_couts[numero_base][coord_x][coord_y])
						liste_nouveau_chemin.append(case)
						matrice_a_remplir_chemin[numero_base][coord_x][coord_y]=list(liste_nouveau_chemin)
						for i in range(4):
							pos_x=coord_x
							pos_y=coord_y
							pos_x+= liste_des_voisins_possible[i][0]
							pos_y+= liste_des_voisins_possible[i][1]
							position_aux=(pos_x,pos_y)
							liste_voisins=list(liste_nouveau_chemin)
							miseajour_carte_chemin_aux(numero_base,matrice_a_remplir_chemin,matrice_de_couts,position_aux,liste_voisins,nb_cases_l,nb_cases_h,fonction_chemin)

	def miseajour_carte_couts_bases2(self):
		for k in range(len(self._pos_bases)):
			base=self.get_base(k)
			position_base=base.position
			miseajour_carte_couts_aux(k,self.carte_couts,position_base,0,self.nb_cases_l,self.nb_cases_h,self.est_case_chemin)

	def miseajour_carte_chemin1(self):
		for k in range(len(self._pos_bases)):
			base=self.get_base(k)
			position_base=base.position
			case=(position_base[0],position_base[1],self.carte_couts[k][position_base[0]][position_base[1]])
			print("dans mise à jour la base est reconnue dans chemin ou non?")
			print(self.est_case_chemin(position_base))
			miseajour_carte_chemin_aux(k,self._carte_des_chemins,self.carte_couts,position_base,[],self.nb_cases_l,self.nb_cases_h,self.est_case_chemin)
