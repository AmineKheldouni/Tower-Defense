#!/usr/bin/python
#encoding: utf8
import random
from csvuser import *

class Vague(object):
    """Gère les vagues d'ennemis
    Le vecteur nb_ennemis contient le nombre d'ennemis encore à apparaître pour chauque id, la case 0
    correspond à une pause et une apparation d'aucun ennemis.
    actualise est la réelle utilité de Vague, elle renvoie les ennemis à créer.
     """
    def __init__(self,id_vague=1, nb_ennemis = 4, nb_source=3):
        self._nb_ennemis = [ExtractIntFromFile("data_vague.csv", id_vague,col) for col in range(1,nb_ennemis+2)]
        self._nb_tot_ennemis = 0
        for i in range(1,len(self._nb_ennemis)):
            self._nb_tot_ennemis += self._nb_ennemis[i]
        self._nb_source     = nb_source

    def decrease(self,id_decrease):
        """ Diminue le compteur correspondant à une pause ou un ennemis"""
        assert(self._nb_ennemis[id_decrease]>0)
        self._nb_ennemis[id_decrease] -= 1
        if(id_decrease>0):
            self._nb_tot_ennemis-= 1

    def get_nb_ennemis(self,indice):
        return self._nb_ennemis[indice]

    def renvoie_soldat(self):
        """Renvoie (id_soldat, id_source), l'id et la source étant aléatoires"""
        if(self.is_over()):
            # print("was over before")
            return 0
        indice =0
        value_indice = self.get_nb_ennemis(0)
        value_rand = random.randint(1,self._nb_tot_ennemis+value_indice)
        #value_rand = 1
        while(value_indice < value_rand):
            indice+=1
            value_indice+= self.get_nb_ennemis(indice)
        self.decrease(indice)
        return indice

    def is_over(self):
        return self._nb_tot_ennemis==0


#  nb ennemis
#  temps
#  niveau ennemis
#  source
