#!/usr/bin/python
#encoding: utf8


from case import *



class Etat(object):
    def  __init__(self,temps,nom,graphic, est_actif=False):
        self._animation = temps
        self._nom = nom
        self._graphic = graphic
        self._est_actif = est_actif
    def valeur_debut(self):
        return []
    def valeur_actualise(self):
        return []
    def valeur_fin(self):
        return []
#Ne changer cette fonction pour aucun état
    def actualisation(self):
        if(self._temps>0):
            self._temps-=1;
            return self.valeur_actualise()
        if(temps==0):
            self._est_actif =0
            return self.valeur_fin()

class Etat_0(Etat):
    """docstring for Etat_0."""
    def __init__(self):
        super(Etat_0, self).__init__(0,"PasEtat","NoImage",0)

class Emplacement(Case):
	def __init__(self, position, tapis, id_excel):
		super(Emplacement,self).__init__(position, "place_construction", tapis,id_excel)

class Glace(Etat):
    def __init__(self):
        super(Glace,self).__init__(9,"glace","feu")
    def debut(self):
        return [("v",2)]
    def fin(self):
        return [("v",1/2)]
'''
Objet Interraction
'''

class Objet_Actif(Case):
    """docstring for Objet_Actif(Case  def __init__(self, arg):"""
    def __init__(self,position,type_objet,id_excel):
        super(Objet_Actif,self).__init__(position,type_objet,0,id_excel)
        self._vie=100
        self._vi=100
        self._etat = Etat_0()
    def active_etat(self):
        for i in range(len(self._etat)):
            if(self._etat[i]._est_actif):
                self.affecte(self._etat[i].valeur_actualise())

    def affecte(self, vect_effets):
        for i in range(len(vect_effets)):
            if(vect_effets[0]=="v"):
                self._vitesse/=vect_effets[i][1]
            if(vect_effets[0]=="p"):
                self._pv+=vect_effets[i][1]
