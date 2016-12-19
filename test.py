#!/usr/bin/python
#encoding: utf8

import PIL
from PIL import Image

basewidth = 10
img = Image.open("images/tours/balle.png")
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
img.save("images/tours/balle.png")
