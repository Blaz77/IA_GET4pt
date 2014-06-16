#from random import randrange,randint
class Simulador(object):
	""" Motores de simulacion de probabilidades para situaciones aleatorias"""
	def __init__(self, probabilidad = 0):
		self.probabilidad = probabilidad
	
	def ataque_individual(self, dado, atacante, atacado, minatk = 1, mindef = 0): 
		""" Recibe un dado, la cantidad de ejercitos de cada lado, 
		un minimo de ejercitos a conservar, y un minimo de 
		ejercitos enemigos a destruir. Devuelve True si 
		consigue destruir el minimo de ejercitos enemigos 
		o False si no lo logra para cuando le quedan igual 
		o menos ejercitos que el minimo.
		"""
		# Para este tipo de funciones la recursividad no es muy buena, ya que el
		# regreso no se aprovecha. Si llega a funcionar lento seria bueno modificarla
		if atacado <= mindef:
			return True
		elif atacante <= minatk:
			return False
		else:
			dado.lanzar_dados(atacante, atacado)
			return self.ataque_individual(dado, atacante - dado.ejercitos_perdidos_atacante(), \
					atacado - dado.ejercitos_perdidos_atacado(), minatk, mindef)

	def chances_ataque(self, dado, atacante, atacado, minatk = 1, mindef = 0, precision = 1000):
		""" Corre mil veces la funcion ataque_individual, y 
		devuelve la probabilidad (estimada) de victoria con 
		esos ejercitos y limites
		"""
		ganados = 0
		for i in xrange(precision):
			gane_combate = self.ataque_individual(dado, atacante, atacado, minatk, mindef)
			if gane_combate:
				ganados += 1
		return ganados*1.0 / precision
