
from constantes import *
from jugador import Jugador

class JugadorInteligente(Jugador):
	"""
	Este jugador va a ganar el torneo!

	(Escribir codigo de aca para abajo)
	"""

	def _limita_con(self, tablero, pais, condicion):
		""" Recibe un pais, devuelve True si 
		algun limite cumple con la condicion.
		"""
		if not self.es_mi_pais(tablero, pais):
			raise ValueError("No es tu pais!")
		for limitrofe in tablero.paises_limitrofes(pais):
			if condicion(tablero, limitrofe):
				return True
		return False
	
	def es_mi_pais(self, tablero, pais):
		return self.color == tablero.color_pais(pais)
	
	def es_enemigo(self, tablero, pais):
		return not self.es_mi_pais(tablero, pais)

	def es_frontera(self, tablero, pais):
		""" Devuelve True si el pais limita con algun pais enemigo.
		"""
		return self._limita_con(tablero, pais, self.es_enemigo)
		
	def es_frontera_unica(self, tablero, pais):
		""" Devuelve True si el pais es frontera y 
		no limita con ninguna otra.
		"""
		es_frontera = self.es_frontera(tablero, pais)
		if not es_frontera:
			return False
		return not self._limita_con(tablero, pais, self.es_frontera)
		
	def es_orden2(self, tablero, pais):
		""" Devuelve True si el pais no es frontera pero 
		es limitrofe con alguna de tus fronteras.
		"""
		es_frontera = self.es_frontera(tablero, pais)
		if es_frontera:
			return False
		return self._limita_con(tablero, pais, self.es_frontera)
	
	def es_orden3(self, tablero, pais):
		""" Devuelve True si el pais no es frontera ni 
		de orden 2 pero limita con alguno de orden 2.
		"""
		es_frontera = self.es_frontera(tablero, pais)
		es_orden2 = self.es_orden2(tablero, pais)
		if es_frontera or es_orden2:
			return False
		return self._limita_con(tablero, pais, self.es_orden2)
	
	def es_seguro(self, tablero, pais):
		""" Deuvelve True si el pais no puede 
		ser atacado en el siguiente turno.
		"""
		es_frontera = self.es_frontera(tablero, pais)
		es_orden2 = self.es_orden2(tablero, pais)
		es_orden3 = self.es_orden3(tablero, pais)
		return not (es_frontera or es_orden2 or es_orden3)
		
		
