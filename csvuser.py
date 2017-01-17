#!/usr/bin/python
#encoding: utf8

import csv

#Retourne dans un tableau de tableaux les élements du fichier csv
#compris dans la zone (i_min,j_min)-(i_max,j_max)
def LoadIntFromFile(name_file,i_min,i_max,j_min,j_max):
    tab=[]
    with open("data/"+name_file,'r') as fichier:
        csv_file=csv.reader(fichier)
        cpt_ligne=-1
        for ligne in csv_file:
            cpt_ligne+=1
            if cpt_ligne>=i_min:
                if cpt_ligne>i_max:
                    break
                else :
                    l=[]
                    for i in range(len(ligne)):
                        if i>=j_min:
                            if i>j_max:
                                break
                            else:
                                l.append(int(ligne[i]))
                    tab.append(l)
        return tab

#Retourne le terme en position (i,j) du fichier csv
#Renvoit None s'il n'existe pas
def ExtractFromFile(name_file,i,j):
    with open("data/"+name_file,'r') as fichier:
        csv_file=csv.reader(fichier)
        cpt=-1
        for ligne in csv_file:
            cpt+=1
            if cpt==i:
                if j<len(ligne):
                    return ligne[j]
        return None

def ExtractIntFromFile(name_file,i,j):
    if ExtractFromFile(name_file,i,j)!=None:
        return int(ExtractFromFile(name_file,i,j))
    return None


def ExtractStrFromFile(name_file,i,j):
    if ExtractFromFile(name_file,i,j)!=None:
        return str(ExtractFromFile(name_file,i,j))
    return None

#Crée le dictionnaire qui associe aux clés en col_1 les valeurs en col_2
#(situés entre ligne_debut et ligne_fin)
#La fonction suppose que de tels élements existent
def DicoFromFile(name_file,ligne_debut,ligne_fin,col_1,col_2):
    with open("data/"+name_file,'r') as fichier:
        csv_file=csv.reader(fichier)
        dico_carte={}
        cpt_ligne=-1
        for ligne in csv_file:
            cpt_ligne+=1
            if cpt_ligne>=ligne_debut:
                if cpt_ligne>ligne_fin:
                    break
                else :
                    cle=None
                    valeur=None
                    for i in range(len(ligne)):
                        if i==col_1:
                            cle=ligne[i]
                        if i==col_2:
                            valeur=ligne[i]
                        if ((cle!=None) and (valeur!=None)):
                            dico_carte[int(cle)]=str(valeur)
        return dico_carte

def affiche(tab):
    for i in range(len(tab)):
        s=""
        for j in range(len(tab[i])):
            s+=str(tab[i][j])+","
        print(s+"\n")

def affiched(dico):
    for cle,valeur in dico.items():
        print(str(cle)+","+str(valeur)+"\n")

#affiche(LoadFromFile("cartes_carte1.csv",1,40,1,50))
#print(ExtractFromFile("cartes_carte1.csv",3,2))
#affiched(DicoFromFile("cartes_legend.csv",2,7,0,1))
