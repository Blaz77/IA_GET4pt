from constantes import *

class Interfaz(object):
	"""Implementacion de la interfaz de usuario del TEG."""

	@staticmethod
	def iniciar(paises, tablero, fondo):
		"""Inicia la interfaz grafica. Recibe un diccionario con las
		coordenadas de cada pais, el nombre de la imagen de fondo del
		tablero y el color de fondo de la ventana."""
		pass

	@staticmethod
	def esta_corriendo():
		"""Informa si la ventana aun esta corriendo."""
		return True

	@staticmethod
	def setear_titulo(titulo):
		"""Establece el titulo del tablero."""
		pass#print titulo

	@staticmethod
	def setear_texto(texto):
		"""Establece el texto del tablero."""
		pass#print texto

	@staticmethod
	def alertar(titulo, texto):
		"""Abre una ventanita de informacion con el titulo y el texto
		seleccionados."""
		print titulo, texto

	@staticmethod
	def actualizar(tablero):
		"""Recibe un diccionario de pares (color, ejercitos) por pais
		y los muestra en el tablero."""
		pass
