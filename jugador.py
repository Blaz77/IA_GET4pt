
from constantes import *

class Jugador(object):
	"""Representa a un jugador de TEG."""
	def __init__(self, color, nombre):
		"""Crea un jugador desde un color y un nombre."""
		self.color = color
		self.nombre = nombre

	def ronda_iniciada(self, tablero, ronda, orden_ronda):
		"""Esta funcion se llama cada vez que comienza una nueva ronda,
		justo antes de que juegue el primer jugador de la ronda.

		Agrumentos:
			tablero: instancia de Tablero
			ronda: numero de la ronda (la primera es la ronda 1).
			orden_ronda: lista de colores, que indica el orden en que
				los jugadores jugaran la ronda.

		Nota: esta funcion existe para que el jugador pueda definir su
		estrategia en base al orden de la ronda. No es necesario
		que realice ninguna accion, y el valor de retorno se ignora.
		"""
		pass

	def atacar(self, tablero, paises_ganados_ronda):
		"""Indica la intencion de atacar un pais, o bien de finalizar
		la fase de ataque.

		Agrumentos:
			tablero: instancia de Tablero
			paises_ganados_ronda: lista de los paises que el jugador ha
				ganado desde que comenzo la ronda.

		Devuelve None si el jugador no quiere atacar, o un par
		(atacante, atacado) en caso contrario."""
		raise NotImplementedError()

	def mover(self, desde, hacia, tablero, paises_ganados_ronda):
		"""Mover ejercitos luego de ganar un pais. Esta funcion se llama
		cada vez que se conquista un pais luego de atacarlo.

		Agrumentos:
			desde: pais atacante
			hacia: pais atacado, que ha sido conquistado
			tablero: instancia de Tablero
			paises_ganados_ronda: lista de los paises que el jugador ha
				ganado desde que comenzo la ronda.

		Devuelve la cantidad de ejercitos que se desea mover al pais
		conquistado. El numero debe ser no menor que 1 y no mayor que 3,
		y el pais atacante debe quedar con al menos 1 ejercito.
		"""
		return 1

	def tarjeta_recibida(self, pais):
		"""Esta funcion se llama cada vez que el jugador recibe una tarjeta.

		Agrumentos:
			pais: Pais de la tarjeta.

		Nota: esta funcion existe para que el jugador pueda definir su
		estrategia en base a las tarjetas recibidas. No es necesario
		que realice ninguna accion, y el valor de retorno se ignora.
		"""
		pass

	def tarjeta_usada(self, pais):
		"""Esta funcion se llama cada vez que el jugador usa una tarjeta
		para incorporar 2 ejercitos en un pais.

		Agrumentos:
			pais: Pais de la tarjeta.

		Nota: esta funcion existe para que el jugador pueda definir su
		estrategia en base a las tarjetas usadas. No es necesario
		que realice ninguna accion, y el valor de retorno se ignora.
		"""
		pass

	def tarjetas_canjeadas(self, paises):
		"""Esta funcion se llama cada vez que el jugador canjea
		3 tarjetas por ejercitos.

		Agrumentos:
			paises: Lista de paises de las tarjetas canjeadas.

		Nota: por simplificacion, el canje de tarjetas automaticamente
		cuando el jugador posee 3 tarjetas canjeables.
		Esta funcion existe para que el jugador pueda definir su
		estrategia en base a las tarjetas canjeadas. No es necesario
		que realice ninguna accion, y el valor de retorno se ignora.
		"""
		pass

	def agregar_ejercitos(self, tablero, cantidad):
		"""Agregar ejercitos en el tablero.

		Agrumentos:
			tablero: instancia de Tablero
			cantidad: diccionario {continente: cantidad}
				Por ejemplo, si cantidad = {"": 2, "Africa": 3}, eso significa
				que el jugador debe a poner 5 ejercitos en sus paises, de los
				cuales 3 tienen que estar obligatoriamente en Africa.

		Devuelve un diccionario {pais: cantidad}. Por ejemplo,
		{"Zaire": 4, "Italia": 1}.
		"""
		raise NotImplementedError()

	def reagrupar(self, tablero, paises_ganados_ronda):
		"""Reagrupar ejercitos.

		Agrumentos:
			tablero: instancia de Tablero
			paises_ganados_ronda: lista de los paises que el jugador ha
				ganado desde que comenzo la ronda.

		Devuelve una lista de tuplas (desde, hacia, cantidad).

		Solo se podran reagrupar ejercitos a paises limitrofes, nunca
		un pais podra quedar vacio.
		Un ejemplo de devolcion de esta funcion puede ser:
		[('Argentina', 'Uruguay', 2), ('Argentina', 'Brasil', 1),
			('Chile', 'Argentina', 1)]
		Esto significa que de Argentina se reagrupan 3 ejercitos, 2 con
		destino a Uruguay y 1 con destino a Brasil. Argentina tiene que
		tener al menos 4 ejercitos. De Chile se pasa uno a Argentina,
		por lo que Chile tiene que tener al menos 2. Todos los paises
		tienen que pertenecer al jugador. Despues de implementado el
		reagrupamiento, Brasil quedara con 1 ejercito mas, Uruguay con
		2 mas, Argentina con 2 menos (salen 3, entra 1) y Chile con 1
		menos."""
		return []

	def _cambiar(self, reagrupamientos, cambios):
		"""Plagiado vilmente del TP3 y usado por el metodo 
		reagrupar, modifica el diccionario de cambios a 
		partir de la lista de reagrupamientos
		"""
		cambios.clear()
		for migracion in reagrupamientos:
			cambios[migracion[0]] = cambios.get(migracion[0], 0) - migracion[2]
			cambios[migracion[1]] = cambios.get(migracion[1], 0) + migracion[2]
		return cambios

	def __str__(self):
		"""Representacion de un jugador."""
		return '%s (%s)' % (self.nombre, NOMBRE_COLORES[self.color])

