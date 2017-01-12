#!/usr/bin/python
#encoding: utf8

from scvuser import *

class Carte_Cout():
    """docstring for Carte_Cout."""
    def __init__(self,longueur, largeur, id_carte):
        cout_case=[[ 1 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
        cout_chemin=[[ 1 for i in range(self._nb_cases_h)] for j in range(self._nb_cases_l)]
