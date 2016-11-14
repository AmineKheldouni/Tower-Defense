#!/usr/bin/python
#encoding: utf8

from armee import *

class Tour:
	def __init__(self, position, projectile,hp = 10, portee = 400, cout_construction=10, \
	cout_entretien=2, cout_amelioration = 50, id_tour=1):
		self._projectile = projectile
		self._vie = hp
		self._portee = portee
		self._cout_construction = cout_construction
		self._cout_entretien = cout_entretien
		self._cout_amelioration = cout_amelioration
		self._id_tour = id_tour
		self._position = position
	# A COMPLETER
