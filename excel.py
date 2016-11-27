#!/usr/bin/python
#encoding: utf8

'''
Atttention
Executer ce fichier créera un nouveau Excel data vide de tout ce qui a été remplit
sauf si vous enlever la ligne 61 ou ---book.save("data.xls")---
'''

from xlwt import Workbook


import xlrd
# ouverture du fichier Excel
wb = xlrd.open_workbook('data.xls')
# création
book = Workbook()

# création de la feuille 1

# Ennemis
feuil1 = book.add_sheet('armee')
feuil1.write(0,0,'id')
feuil1.write(0,1,'nom')
feuil1.write(0,2,'pv')
feuil1.write(0,3,'defense')
feuil1.write(0,4,'vitesse')
feuil1.write(0,5,'attaque')

# ajout des valeurs dans la ligne suivante
ligne1 = feuil1.row(1)
ligne1.write(1,'Bowser')
ligne1.write(0,'1')
ligne1.write(2,'100')
ligne1.write(3,'1')
ligne1.write(4,'1')
ligne1.write(5,'1')
ligne1.write(6,'bowser.jpg')
# ajustement éventuel de la largeur d'une colonne
feuil1.col(0).width = 10000

# éventuellement ajout d'une autre feuille 2
feuil2 = book.add_sheet('tourelle')
feuil2.write(0,0,'id')
feuil2.write(0,1,'nom')
feuil2.write(0,2,'pv')
feuil2.write(0,3,'defense')
feuil2.write(0,4,'vitesse')
#projectile donne l'ID du projectile
feuil2.write(0,5,'projectile')

feuil3 = book.add_sheet('projectile')
feuil3.write(0,0,'id')
feuil3.write(0,1,'nom')
#si le projectile est un gaz ou un cercle de feu
feuil3.write(0,2,'rayon')
feuil3.write(0,3,'vitesse')
feuil3.write(0,4,'vitesse')
#projectile donne l'ID du projectile

book.save("data.xls")
'''
Lourd, il faut ouvrir tout le temps le doc c'est peut-être lent
data_python peut être global
'''

def extract(feuille,id_data,donnee):
#id correspond à la ligne
#donne est la colonne (entier)
    wb = xlrd.open_workbook('data.xls')
    sh=wb.sheet_by_name(feuille)
    return sh.col_values(donnee)[id_data]

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

print(extract2("armee",1,"pv"))
# création matérielle du fichier résultant
book.save('data.xls')
