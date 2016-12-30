#!/usr/bin/python
#encoding: utf8

class Case(object):
	def __init__(self, position, type_objet="",tapis=0, id_graphic=0, is_chemin=0):
		self._position = position
		self._type_objet = type_objet # String de legend2
		self._tapis = tapis	# Int de legend1
		self._id_graphic = id_graphic
		self._est_chemin = is_chemin
	@property
	def position(self):
		return self._position
	@property
	def type_objet(self):
		return self._type_objet
	@property
	def tapis(self):
		return self._tapis
	@property
	def __setitem__(self, objet_id):
		self._type_objet = objet_id
	def set_id(self,new_id):
		self._id_graphic = new_id
	def est_attackable(self):
		return False
	@property
	def __getitem__(self):
		return self.type_objet
	def actualisation(self):
		None
	#Dis si l'armée peut marcher dessus
	def est_chemin(self, dir_soldat=0):
		if(self._est_chemin==1):
			return True
		if (self._est_chemin==-(dir_soldat+1)):
			return True
		else:
			return False

class Emplacement(Case):
	def __init__(self, position, tapis, id_excel):
		super(Emplacement,self).__init__(position, "place_construction", tapis,id_excel)

# Pour faire un No_Objet : (self,position,graphic,arg,id_exel)
class Element_decor(Case):
	"""docstring for Element_decor."""
	def __init__(self, position, tapis, id_excel):
		super(Element_decor,self).__init__(position,"element_decor",tapis,id_excel)

class Source(Case):
	"""docstring for Element_decor."""
	def __init__(self, position, tapis, id_excel):
		super(Source,self).__init__(position,"source",tapis,id_excel)

class Base(Case):
	def __init__(self, position, tapis=0,id_excel=103):
	 	super(Base,self).__init__(position,"base",tapis,id_excel,0)
	 	self.vie_depart = 20
		self._vie = self.vie_depart
		self._cout_entretien = 100
		self._cout_amelioration = 20
		self._est_mort = False
	@property
	def vie(self):
		return self._vie
	@property
	def position(self):
	 	return self._position
	# def est_morte(self):
	# 	if self.vie == 0:
	# 		return True
	# 	return False

	def is_attackable(self):
		return self._vie>0
	def dommage(self,degat):
		self._vie -= degat
		self._vie = max(0,self._vie)
	def actualisation(self):
		if(not self._est_mort):
			if self._vie > self.vie_depart/2:
				self.set_id(103)
			elif self._vie >self.vie_depart/5 and self._vie <=self.vie_depart/2:
				self.set_id(104)
			else:
				self.set_id(105)
			if(self._vie==0):
				self._est_mort=True
				return True
			else:
				return False
		else:
			return False

	def ameliorer(self):
		if self._joueur.argent >= self._cout_entretien:
			self._vie += 1
			self._joueur.argent -= self._cout_entretien
# = liste_entretien_base[id_entretien+1] => Creer une liste de couts
#d'entretiens sur un Excel, pour augmenter le cout
			self._cout_entretien += 1
