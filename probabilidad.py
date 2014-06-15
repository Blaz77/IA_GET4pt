from constantes_probabilidad import *
from manejo_datos import csv_a_diccionario, agregar_probabilidad
class Probabilidad(object):
	"""Coleccion de motores de probabilidades teoricas"""
	def __init__(self, ultima_probabilidad = 0):
		self.ultima_probabilidad = ultima_probabilidad
	
	def ataque(self, atacante, atacado, minatk = 1, maxdef = 0, nombre_archivo = "base.csv"):
		if atacado != int(atacado) or atacante != int(atacante):
			return 0
		if atacado <= maxdef:
			return 1
		if atacante <= minatk:
			return 0
		base = csv_a_diccionario(nombre_archivo)
		if (atacante, atacado) in base:
			self.ultima_probabilidad =  base[(atacante, atacado)]
			return self.ultima_probabilidad
		else:
			atacantereal = min(atacante, 4)
			atacadoreal = min(atacado, 3)
			chance = CHANCES[(atacantereal, atacadoreal)]
			chancekeys = sorted(chance.keys())
			self.ultima_probabilidad = (chance[chancekeys[0]] * self.ataque(atacante + chancekeys[0][0], atacado + chancekeys[0][1], minatk, maxdef, nombre_archivo) +
						    chance[chancekeys[1]] * self.ataque(atacante + chancekeys[1][0], atacado + chancekeys[1][1], minatk, maxdef, nombre_archivo) +
						    chance[chancekeys[2]] * self.ataque(atacante + chancekeys[2][0], atacado + chancekeys[2][1], minatk, maxdef, nombre_archivo) +
						    chance[chancekeys[3]] * self.ataque(atacante + chancekeys[3][0], atacado + chancekeys[3][1], minatk, maxdef, nombre_archivo))
			agregar_probabilidad(nombre_archivo, atacante, atacado, self.ultima_probabilidad)
			return self.ultima_probabilidad
	def ver_ultimo_calculo(self):
		return self.ultima_probabilidad
