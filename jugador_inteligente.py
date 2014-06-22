
from constantes import *
from jugador import Jugador

class JugadorInteligente(Jugador):
	"""
	Este jugador va a ganar el torneo!

	(Escribir codigo de aca para abajo)
	"""
	#Dejo aca los metodos lindos rapidos y usados (casi) por todas las AI.
	def _limita_con(self, tablero, pais, condicion):
		""" Recibe un pais, devuelve True si 
		algun limite cumple con la condicion.
		"""
		for limitrofe in tablero.paises_limitrofes(pais):
			if condicion(tablero, limitrofe):
				return True
		return False
	
	def es_mi_pais(self, tablero, pais):
		return self.color == tablero.color_pais(pais)
	
	def es_enemigo(self, tablero, pais):
		return not self.es_mi_pais(tablero, pais)
	
	def es_frontera(self, tablero, pais):
		""" Recibe un pais aliado, devuelve 
		True si limita con algun pais enemigo.
		"""
		return self._limita_con(tablero, pais, self.es_enemigo)
	
	def es_amenaza(self, tablero, pais):
		""" Recibe un pais enemigo, devuelve True 
		si limita con alguno de los paises aliados.
		"""
		if self.es_mi_pais(tablero, pais):
			raise ValueError("Es mi pais!")
		return self._limita_con(tablero, pais, self.es_frontera)
	
	def es_frontera_unica(self, tablero, pais):
		""" Devuelve True si el pais es frontera y 
		no limita con ninguna otra.
		"""
		es_frontera = self.es_frontera(tablero, pais)
		if not es_frontera:
			return False
		return not self._limita_con(tablero, pais, self.es_frontera)
		
	def es_seguro(self, tablero, pais):
		""" Deuvelve True si el pais no puede 
		ser atacado en el siguiente turno.
		"""
		orden_proteccion = self.orden_proteccion(tablero)
		return orden_proteccion[pais] > 3

	@staticmethod #Para definir funciones que no utilizan al objeto.
	def cambios(reagrupamientos):
		"""Plagiado vilmente del TP3 y usado por el metodo 
		reagrupar, modifica el diccionario de cambios a 
		partir de la lista de reagrupamientos
		"""
		cambios = {}
		for migracion in reagrupamientos:
			cambios[migracion[0]] = cambios.get(migracion[0], 0) - migracion[2]
			cambios[migracion[1]] = cambios.get(migracion[1], 0) + migracion[2]
		return cambios

	def orden_proteccion(self, tablero):
		""" Devuelve un diccionario con tus paises 
		de clave y la cantidad de paises que 
		lo protegen (incluyendose) como valor.
		"""
		orden_proteccion = {}
		paises = tablero.paises_color(self.color)
		for pais in paises:
			if self.es_frontera(tablero, pais):
				orden_proteccion[pais] = 1
			else:
				orden_proteccion[pais] = 100 #Numero absurdo: El maximo orden es 9 o 10
		while 100 in orden_proteccion.values():
			for pais in orden_proteccion:
				for limitrofe in tablero.paises_limitrofes(pais):
					if limitrofe not in paises:
						continue
					orden_proteccion[limitrofe] = min(orden_proteccion[limitrofe], orden_proteccion[pais]+1)
		return orden_proteccion
