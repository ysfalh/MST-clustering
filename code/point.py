from math import sqrt 

class Point:
	def __init__(self, _numero, _dim, _name):
		self.numero = _numero
		self.name = _name
		self.coords = [0]*_dim


	def print_point(self):
		print("Numero =", self.numero)
		print("Name =", self.name)

	def euclidian_dist(self, q):  #q est de type Point
		sqd = 0
		dim = len(self.coords)
		for m in range(dim):
			sqd += (self.coords[m]-q.coords[m]) * (self.coords[m]-q.coords[m])
		return round(sqrt(sqd),2)