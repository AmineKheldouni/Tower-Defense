#!/usr/bin/python
#encoding: utf8

'''
Crée une classe mère de tout objet avec lesquels on peut interragir
Arg est idéalement une fonction qu'on appelle quand on clique sur l'objet
'''
from excel import *
class Objet_Interraction(object):
    def __init__(self,position,id_exel=0,arg=0,is_graphic=False):
        self._is_graphic = is_graphic
        self._id_exel=id_exel
        self._interraction = arg
        self._position =position
        @property
        def position(self):
            return self._position
        @property
        def id_exel(self):
            return self._id_exel

#
# class ClassName(object):
#     """docstring for ."""
#     def __init__(self, arg):
#         super(, self).__init__()
#         self.arg = arg
#
