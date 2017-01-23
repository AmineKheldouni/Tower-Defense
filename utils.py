#!/usr/bin/python
#encoding: utf8



def affiche_tableau(vecteur):
    stig = ""
    for j in range(len(vecteur[0])):
        strig = ""
        for i in range(len(vecteur)):
            strig = strig +"|"+ str(vecteur[i][j])
        print(strig)
