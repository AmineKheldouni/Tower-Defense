#!/usr/bin/python
#encoding: utf8

# import PIL
# from PIL import Image
#
# basewidth = 10
# img = Image.open("images/tours/balle.png")
# wpercent = (basewidth/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
# img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
# img.save("images/tours/balle.png")

from csvuser import *

def main():
    id_carte = "cartes_carte4"
    nb_cases_h = ExtractIntFromFile(id_carte+".csv",0,1)
    nb_cases_l = ExtractIntFromFile(id_carte+".csv",0,2)
    tab_carte=LoadIntFromFile(id_carte+".csv",1,nb_cases_l,1, nb_cases_h)
    tab_carte_objets=LoadIntFromFile(id_carte+"objets.csv",1,nb_cases_l,1, nb_cases_h)
    new_rows = [] # a holder for our modified rows when we make them
    new_rows_ob =[]
    print(tab_carte)
    print(tab_carte_objets)
    with open('data/data_score.csv', 'rb') as f1:
        reader = csv.reader(f1) # pass the file to our csv reader
        for i in range(len(tab_carte[0])):     # iterate over the rows in the file
            new_row = []
            new_row_ob = []
            for j in range(len(tab_carte)):
                print(new_row)
                new_row.append(tab_carte[j][i])
                new_row_ob.append(tab_carte[j][i])
            new_rows.append(new_row)
            new_rows_ob.append(new_row_ob)
    with open('data/cartes_carte5.csv', 'wb') as f2:
        # Overwrite the old file with the modified rows
        writer = csv.writer(f2)
        writer.writerows(new_rows)
    with open('data/cartes_carte5objets.csv', 'wb') as f2:
        # Overwrite the old file with the modified rows
        writer = csv.writer(f2)
        writer.writerows(new_rows_ob)

main()
