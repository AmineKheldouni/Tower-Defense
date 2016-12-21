from excel import *

'''
Ce document sert à gérer un certain  nombre de paramètres globaux non modifiables comme certain dictionnaire et l'ouverture
des documents excel qui est très longue
''''
dico_carte=cree_dico('legend',1,2)
dico_carte_object=cree_dico('legend2',1,2)
dico_nom_id=cree_dico('legend2',1,0)
data_exel = open_workbook("data.xls")
carte_exel= open_workbook("cartes.xls")


class Global_fct(object):
    @staticmethod
    def f(x,y)
