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

def give_score(nb_score=10):
    with open("data/data_score.csv",'r') as fichier:
        score = []
        csv_file=csv.reader(fichier)
        cpt_ligne=-1
        for ligne in csv_file:
            cpt_ligne+=1
            score.append( ( int(ligne[0]), str(ligne[1]), int(ligne[2]) )  )
            if(cpt_ligne >nb_score):
                    break
        return score

def enter_new_score(player, player_score):
        add_row = [0,player, player_score]
        new_rows = [] # a holder for our modified rows when we make them
        pivot_row = []
        with open('data/data_score.csv', 'rb') as f1:
            reader = csv.reader(f1) # pass the file to our csv reader
            for row in reader:     # iterate over the rows in the file
                new_row = row      # at first, just copy the row
                if( int(add_row[2]) > int(new_row[2]) ):
                    print("hello")
                    pivot_row = [new_row[0], new_row[1], new_row[2]]
                    new_row = [new_row[0], add_row[1], add_row[2]]
                    add_row = [pivot_row[0], pivot_row[1] ,pivot_row[2]]
                new_rows.append(new_row) # add the modified rows
        with open('data/data_score.csv', 'wb') as f2:
            # Overwrite the old file with the modified rows
            writer = csv.writer(f2)
            writer.writerows(new_rows)

#affiche(LoadFromFile("cartes_carte1.csv",1,40,1,50))
#print(ExtractFromFile("cartes_carte1.csv",3,2))
#affiched(DicoFromFile("cartes_legend.csv",2,7,0,1))
