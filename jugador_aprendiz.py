# Practicando implementaciones de jugador
# Este jugador sigue algunas reglas del archivo de inteligencia

from constantes import *
from jugador import Jugador
from probabilidad import Probabilidad, proba

class JugadorAprendiz(Jugador):
	""" Primer prototipo de un jugador inteligente.
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
	
	def agregar_ejercitos(self, tablero, cantidad):
		# Esto tiene el problema de que agrega ejercitos en bloque.
		jugada = {}
		for continente, cantidad_continente in sorted(cantidad.items(), reverse=True):
			paises_posibles = tablero.paises(continente)
			for i, pais in enumerate(paises_posibles):
				if tablero.color_pais(pais) != self.color:
					continue
				# Si en todos da False, agrega en el ultimo
				if i != len(paises_posibles) - 1 and not self.quiero_agregar(tablero, pais):
					continue
				jugada[pais] = jugada.get(pais, 0) + cantidad_continente
				break
		return jugada
		
	def quiero_agregar(self, tablero, pais):
		""" Informa si el pais es una buena opcion para agregar ejercitos """
		# Quiero agregar si algun pais vecino es enemigo
		return self.es_frontera(tablero, pais)
	
	def atacar(self, tablero, paises_ganados_ronda):
		mis_paises = tablero.paises_color(self.color)
		for pais in mis_paises:
			for limitrofe in tablero.paises_limitrofes(pais):
				# no me quiero atacar a mi mismo
				if tablero.color_pais(limitrofe) == self.color:
					continue
				# Estrenando las probabilidades
				if self.quiero_atacar(tablero, pais, limitrofe, 0.51):
					return pais, limitrofe
		return None
		
	def quiero_atacar(self, tablero, origen, destino, proba_aceptada):
		""" Informa si el pais de destino es una buena opcion para atacar. Recibe
		la probabilidad de exito aceptable y devuelve True si la probabilidad real
		la iguala o supera.
		"""
		return (proba.ataque(tablero.ejercitos_pais(origen), 
				tablero.ejercitos_pais(destino)) >= proba_aceptada)

	def mover(self, origen, destino, tablero, paises_ganados_ronda):
		""" Se ejecuta al ocupar un pais y devuelve la cantidad de ejercitos
		de ocupacion."""
		# Muevo la mayor cantidad de ejercitos posible.
		return max(1, min(3, tablero.ejercitos_pais(origen) - 1))
	
	def reagrupar(self, tablero, paises_ganados_ronda):
		# Mueve los ejercitos de paises de orden 3 a paises de orden 2
		# Si el pais es de orden 2 y tiene mas de 10 ejercitos, mueve el
		# excedente a paises frontera
		reagrupamientos = []
		mis_paises = tablero.paises_color(self.color)
		for pais in mis_paises:
			if (self.es_orden3(tablero, pais)):
				for limitrofe in tablero.paises_limitrofes(pais):
					if (limitrofe in mis_paises and self.es_orden2(tablero, limitrofe)):
						reagrupamientos.append( (pais, limitrofe, tablero.ejercitos_pais(pais)-1) )
						tablero.actualizar_interfaz(self.cambios(reagrupamientos))
						break
			elif (self.es_orden2(tablero, pais) and tablero.ejercitos_pais(pais) > 10):
				for limitrofe in tablero.paises_limitrofes(pais):
					if (limitrofe in mis_paises and self.es_frontera(tablero, limitrofe)):
						reagrupamientos.append( (pais, limitrofe, tablero.ejercitos_pais(pais)-10) )
						tablero.actualizar_interfaz(self.cambios(reagrupamientos))
						break
		return reagrupamientos
