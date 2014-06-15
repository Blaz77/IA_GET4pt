
from constantes import *
from jugador import Jugador

class JugadorInteligente(Jugador):
	"""
	Este jugador va a ganar el torneo!

	(Escribir codigo de aca para abajo)
	"""

	def _limita_con(self, tablero, pais, paises_ganados_ronda, funcion):
		""" Recibe un pais, devuelve True si 
		un limite cumple con la condicion.
		"""
		if not es_mi_pais:
			raise ValueError("No es tu pais!")
		for limitrofe in tablero.paises_limitrofes(pais):
			if funcion(tablero, limitrofe, paises_ganados_ronda):
				return True
		return False
	
	def es_mi_pais(self, tablero, pais, paises_ganados_ronda):
		return self.color == tablero.color_pais(pais)
	
	def es_enemigo(self,tablero, pais, paises_ganados_ronda):
		return not self.es_mi_pais(self, tablero, pais, paises_ganados_ronda)

	def es_frontera(self, tablero, pais, paises_ganados_ronda):
		""" Devuelve True si el pais limita con algun pais enemigo.
		"""
		return _limita_con(self, tablero, pais, paises_ganados_ronda, self.es_enemigo)
		
	def es_frontera_unica(self, tablero, pais, paises_ganados_ronda):
		"""Devuelve True si el pais es frontera y 
		no limita con ninguna otra.
		"""
		es_frontera = self.es_frontera(self, tablero, pais, paises_ganados_ronda)
		if not es_frontera:
			return False
		return _limita_con(self, tablero, pais, paises_ganados_ronda, self.es_frontera)
		
	def es_orden2(self, tablero, pais, paises_ganados_ronda):
		""" Devuelve True si el pais no es frontera pero 
		es limitrofe con alguna de tus fronteras.
		"""
		es_frontera = self.es_frontera(self, tablero, pais, paises_ganados_ronda)
		if es_frontera:
			return False
		return _limita_con(self, tablero, pais, paises_ganados_ronda, self.es_frontera)
	
	def es_orden3(self, tablero, pais, paises_ganados_ronda):
		""" Devuelve True si el pais no es frontera o 
		de orden 2 pero limita con alguno de orden 2.
		"""
		es_frontera = self.es_frontera(self, tablero, pais, paises_ganados_ronda)
		es_orden2 = self.es_orden2(self, tablero, pais, paises_ganados_ronda)
		if es_frontera or es_orden2:
			return False
		return _limita_con(self, tablero, pais, paises_ganados_ronda, self.es_orden2)
	
	def es_seguro(self, tablero, pais, paises_ganados_ronda):
		"""Deuvelve True si el pais no puede 
		ser atacado en el siguiente turno.
		"""
		es_frontera = self.es_frontera(self, tablero, pais, paises_ganados_ronda)
		es_orden2 = self.es_orden2(self, tablero, pais, paises_ganados_ronda)
		es_orden3 = self.es_orden3(self, tablero, pais, paises_ganados_ronda)
		return not (es_frontera or es_orden2 or es_orden3)
		
		
