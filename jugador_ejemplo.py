
from constantes import *
from jugador import Jugador

class _JugadorEjemplo(Jugador):
	"""
	Clase base de ejemplo de implementacion de Jugador.
	JugadorSuicida y JugadorOfensivo son las dos clases concretas
	que heredan de _JugadorEjemplo.
	"""

	def quiero_atacar(self, desde, hacia, tablero):
		"""Dados dos paises enemigos limitrofes, determina si es una buena opcion
		para atacar"""
		raise NotImplementedError()

	def atacar(self, tablero, paises_ganados_ronda):
		mis_paises = tablero.paises_color(self.color)
		# ordeno por cantidad de ejercitos (mayor a menor)
		mis_paises.sort(key = lambda p: tablero.ejercitos_pais(p), reverse=True)
		for pais in mis_paises:
			if tablero.ejercitos_pais(pais) < 2:
				# no tengo movimientos posibles
				return None
			for limitrofe in tablero.paises_limitrofes(pais):
				#no me quiero atacar a mi mismo
				if tablero.color_pais(limitrofe) == self.color:
					continue
				if self.quiero_atacar(pais, limitrofe, tablero):
					return pais, limitrofe
		return None

	def agregar_ejercitos(self, tablero, cantidad):
		jugada = {}
		for continente, cantidad_continente in sorted(cantidad.items(), reverse=True):
			paises_posibles = tablero.paises(continente)
			for i, pais in enumerate(paises_posibles):
				if tablero.color_pais(pais) != self.color:
					continue
				if i != len(paises_posibles) - 1 and not self.quiero_agregar(pais, tablero):
					continue
				jugada[pais] = jugada.get(pais, 0) + cantidad_continente
				break
		return jugada

class JugadorSuicida(_JugadorEjemplo):
	"""
	Este jugador tiene todas las de perder.
	"""

	def quiero_atacar(self, desde, hacia, tablero):
		""" Informa si el pais 'hacia' es una buena opcion para atacar """
		# Quiero tacar si tengo menos ejercitos (suicida!)
		return tablero.ejercitos_pais(desde) < tablero.ejercitos_pais(hacia) + 2

	def quiero_agregar(self, pais, tablero):
		""" Informa si el pais es una buena opcion para agregar ejercitos """
		return True

class JugadorOfensivo(_JugadorEjemplo):
	"""
	Este jugador es un poquito mas inteligente que el JugadorSuicida.
	"""

	def quiero_atacar(self, desde, hacia, tablero):
		""" Informa si el pais 'hacia' es una buena opcion para atacar """
		# Quiero tacar si tengo mas ejercitos
		return tablero.ejercitos_pais(desde) >= tablero.ejercitos_pais(hacia) + 2

	def quiero_agregar(self, pais, tablero):
		""" Informa si el pais es una buena opcion para agregar ejercitos """
		# Quiero agregar si algun pais vecino es enemigo
		return any(tablero.color_pais(p) != self.color for p in tablero.paises_limitrofes(pais))

	def mover(self, desde, hacia, tablero, paises_ganados_ronda):
		# Muevo todos los ejercitos que puedo
		return max(1, min(3, tablero.ejercitos_pais(desde) - 1))

