#!/usr/bin/python
#encoding: utf8
'''
Document en cours de création

Attention d'après le système de couche (interface, graphique etc) ce Document
n'a pas le droit d'importer autre chose (tourelle, affiche, armée... )

Important :
Fonction Utiles pour les autres docs :
(aucune pour 'linstant')

'''
import xlrd
from xlwt import Workbook
# ouverture du fichier Excel
wb = xlrd.open_workbook('test.xls')

# feuilles dans le classeur
print (wb.sheet_names())
[u'Feuille1', u'Feuille2', u'Feuille3']

# lecture des données dans la première feuille
sh = wb.sheet_by_name(u'Feuille1')
for rownum in range(sh.nrows):
    print(sh.row_values(rownum))
[u'id', u'x', u'y', u'test']
[1.0, 235.0, 424.0, u'a']
[2.0, 245.0, 444.0, u'b']
[3.0, 255.0, 464.0, u'c']
[4.0, 265.0, 484.0, u'd']
[5.0, 275.0, 504.0, u'e']
[6.0, 285.0, 524.0, u'f']
[7.0, 295.0, 544.0, u'g']

# lecture par colonne
colonne1 = sh.col_values(0)
print (colonne1)
[u'id', 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]

colonne2=sh.col_values(1)
print (colonne2)
[u'x', 235.0, 245.0, 255.0, 265.0, 275.0, 285.0, 295.0]

################################################################

# ouverture du fichier Excel
wb = xlrd.open_workbook('test.xls')

# feuilles dans le classeurFeuille
print (wb.sheet_names())
[u'Feuille1', u'Feuille2', u'Feuille3']

# lecture des données dans la première feuille
sh = wb.sheet_by_name(u'Feuille1')
for rownum in range(sh.nrows):
    print (sh.row_values(rownum))
[u'id', u'x', u'y', u'test']
[1.0, 235.0, 424.0, u'a']
[2.0, 245.0, 444.0, u'b']
[3.0, 255.0, 464.0, u'c']
[4.0, 265.0, 484.0, u'd']
[5.0, 275.0, 504.0, u'e']
[6.0, 285.0, 524.0, u'f']
[7.0, 295.0, 544.0, u'g']

# lecture par colonne
colonne1 = sh.col_values(0)
print(colonne1)
[u'id', 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]

colonne2=sh.col_values(1)
print(colonne2)
[u'x', 235.0, 245.0, 255.0, 265.0, 275.0, 285.0, 295.0]

# extraction d'un élément par


# création
book = Workbook()

# création de la feuille 1
feuil1 = book.add_sheet('feuille 1')

# ajout des en-têtes
feuil1.write(0,0,'id')
feuil1.write(0,1,'x')
feuil1.write(0,2,'y')
feuil1.write(0,3,'test')

# ajout des valeurs dans la ligne suivante
ligne1 = feuil1.row(1)
ligne1.write(0,'1')
ligne1.write(1,'235.0')
ligne1.write(2,'424.0')
ligne1.write(3,'a')

# ajustement éventuel de la largeur d'une colonne
feuil1.col(0).width = 10000

# éventuellement ajout d'une autre feuille 2
feuil2 = book.add_sheet('feuille 2')
