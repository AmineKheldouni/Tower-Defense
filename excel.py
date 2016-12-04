#!/usr/bin/python
#encoding: utf8

import xlrd
from xlwt import Workbook


excel_carte = xlrd.open_workbook('cartes.xls')
# ouverture du fichier Excel
excel_data = xlrd.open_workbook('data.xls')
# création
'''
Lourd, il faut ouvrir tout le temps le doc c'est peut-être lent
data_python peut être global
'''

def extract(feuille,id_data,donnee):
#id correspond à la ligne
#donne est la colonne (entier)
    wb = xlrd.open_workbook('data.xls')
    sh=wb.sheet_by_name(feuille)
    return int(sh.col_values(donnee)[id_data])

def extract_string(feuille,id_data,donnee):
#id correspond à la ligne
#donne est la colonne (entier)
    wb = xlrd.open_workbook('data.xls')
    sh=wb.sheet_by_name(feuille)
    return str(sh.col_values(donnee)[id_data])

def extract2(feuille,id_data,donnee):
    wb=xlrd.open_workbook('data.xls')
    sh=wb.sheet_by_name(feuille)
    x=1
    while(x<10):
        if(donnee==sh.col_values(x)[0]):
            return sh.col_values(x)[id_data]
        else:
            x=x+1
    assert(False)
    #vous avez demander une donnée qui n'est pas répertoriée

def extract_carte(id_carte,i,j):
    sh=excel_carte.sheet_by_name(id_carte)
    return int (sh.cell_value(i,j))

def cree_dico(legend):
    wb = xlrd.open_workbook('cartes.xls')
    sh=wb.sheet_by_name(legend)
    dico_carte={}
    for i in range(2,int(sh.col_values(1)[1]+2)):
        dico_carte[sh.cell_value(i,1)] = str(sh.cell_value(i,2))
    return dico_carte

# création matérielle du fichier résultant
