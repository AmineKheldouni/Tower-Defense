#!/usr/bin/python
#encoding: utf8


from case import *

'''
Pour créer un nouvel état il suffit faire une calsse fille et de surcharger les fonctions : valeur_début, valeur_fin et valeur_actualise
utilisées respectivement à l'activation à la fin et à chaque pas de temps
(ainsi que les graphismes)
'''

class Etat(object):
    def  __init__(self,temps,nom):
        self._temps = temps
        self._nom = nom

    def est_actif(self):
        return (self._temps>0)
#Changer ces trois fonctions pour créer un nouvelle etat qui hérite de Etat
    def valeur_debut(self):
        return []
    def valeur_actualise(self):
        return []
    def valeur_fin(self):
        return []
#Ne changer cette fonction pour aucun état
    def actualisation(self):
        self._temps-=1;
        return self.valeur_actualise()

class Etat_0(Etat):
    """docstring for Etat_0."""
    def __init__(self):
        super(Etat_0, self).__init__(0,"0")
    def est_actif(self):
        return True

class Emplacement(Case):
	def __init__(self, position, tapis, id_excel):
		super(Emplacement,self).__init__(position, "place_construction", tapis,id_excel)

class Feu(Etat):
    def __init__(self):
        super(Feu,self).__init__(30,"feu")
    def valeur_debut(self):
        return []
    def valeur_fin(self):
        return [("p",-1)]
    def valeur_actualise(self):
        return []

class Glace(Etat):
    def __init__(self):
        super(Glace,self).__init__(15,"glace")
    def valeur_debut(self):
        return [("v",0.5)]
    def valeur_fin(self):
        return [("v",2)]
    def valeur_actualise(self):
        return []

'''
Objet Interraction
'''

class Objet_Actif(Case):
    """docstring for Objet_Actif(Case  def __init__(self, arg):"""
    def __init__(self,position,type_objet,id_excel):
        super(Objet_Actif,self).__init__(position,type_objet,0,id_excel)
        self._pv=100
        self._vitesse=100
        self._etat = Etat_0()

    def change_etat(self,etat):
        #Enlève l'état précédent
        self.affecte( self._etat.valeur_fin())
        #Change l'état
        self._etat = etat
        #On active l'état
        self.affecte(self._etat.valeur_debut())

    def actualise_etat(self):
        if(self._etat._nom != "0"):
            #Si l'état est actif on l'actualise sinon on remplace par l'Etat_0
            if(self._etat.est_actif()):
                self.affecte(self._etat.actualisation())
            else:
                self.change_etat(Etat_0())

#Permet de traduire les données de Etat en valeur de jeu
    def affecte(self, vect_effets):
        for i in range(len(vect_effets)):
            if(vect_effets[i][0]=="p"):
                self._pv+=vect_effets[i][1]
            elif(vect_effets[i][0]=="v"):
                self._vitesse*=vect_effets[i][1]
