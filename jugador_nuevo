
from constantes import *
from jugador import Jugador
from jugador_inteligente import JugadorInteligente
from probabilidad import proba

class JugadorNuevo(JugadorInteligente):
	""" Nuevo intento de jugador.
	"""
	def __init__(self, color, nombre):
                JugadorInteligente.__init__(self, color, nombre)
                
                # Nocion del tiempo y turno.
                self.ronda = 0
                self.orden_ronda = []
                
                # Inventario del jugador
                self.tarjetas = {}
                self.cantidad_canjes = 0

                # Estrategia
                self.territorios = [] #Aca, supongo, se pondrian listas de territorios conexos.
		self.proba_aceptada = 0
		self.caracter = 0

	def ronda_iniciada(self, tablero, ronda, orden_ronda):
		"""Guarda los valores recibidos como parámetros, a ser usados por
		el jugador en otras ocasiones.
		"""

                self.ronda = ronda
                self.orden_ronda = orden_ronda

	def tarjeta_recibida(self, pais):
		"""Esta funcion se llama cada vez que el jugador recibe una tarjeta.
		"""
		# Este chequeo será inutil una vez q confirmemos que nunca ocurre.
		if pais in tarjetas:
			raise ValueError("Ya la teniamos")
		self.tarjetas[pais] = False

	def tarjeta_usada(self, pais):
		"""Esta funcion se llama cada vez que el jugador usa una tarjeta
		para incorporar 2 ejercitos en un pais.
		"""
		# Este chequeo será inutil una vez q confirmemos que nunca ocurre.
		if pais not in tarjetas:
			raise ValueError("No la teniamos")
		self.tarjetas[pais] = True

	def tarjetas_canjeadas(self, paises):
		"""Esta funcion se llama cada vez que el jugador canjea
		3 tarjetas por ejercitos.
		"""
		for pais in paises:
			self.tarjetas.pop(pais)
		self.cantidad_canjes += 1
                
#	def agregar_ejercitos(self, tablero, cantidad):

#	def quiero_agregar(self, tablero, pais):

#	def atacar(self, tablero, paises_ganados_ronda):

#	def quiero_atacar(self, tablero, origen, destino, proba_aceptada):

#	def mover(self, origen, destino, tablero, paises_ganados_ronda):

#	def reagrupar(self, tablero, paises_ganados_ronda):
