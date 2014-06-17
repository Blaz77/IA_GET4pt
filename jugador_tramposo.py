# Practicando implementaciones de jugador

from constantes import *
from jugador import Jugador

class JugadorTramposo(Jugador):
	""" Jugador que hace trampa.
	"""
	def agregar_ejercitos(self, tablero, cantidad):
		""" Agrega todo al primer pais propio que encuentra."""
		jugada = {}
		for continente, cantidad_continente in sorted(cantidad.items(), reverse=True):
			paises_posibles = tablero.paises(continente)
			for i, pais in enumerate(paises_posibles):
				if tablero.color_pais(pais) != self.color:
					continue
				jugada[pais] = jugada.get(pais, 0) + cantidad_continente
				break
		return jugada
	
	def atacar(self, tablero, paises_ganados_ronda):
		""" Distrae a los otros jugadores y ocupa todos los paises."""
		# El camino mas corto entre dos puntos es en linea recta
		lista_paises = tablero.paises()
		for pais in lista_paises:
			if (self.es_enemigo(tablero, pais)):
				tablero.ocupar_pais(pais, self.color, 3)
		return None
	
	def es_mi_pais(self, tablero, pais):
		return self.color == tablero.color_pais(pais)
	
	def es_enemigo(self, tablero, pais):
		return not self.es_mi_pais(tablero, pais)
