from constantes_probabilidad import *

class Probabilidad(object):
	"""Coleccion de motores de probabilidades teoricas"""
	def __init__(self, ultima_probabilidad = 0):
		self.ultima_probabilidad = ultima_probabilidad
	
	def ataque(self, atacante, atacado, minatk = 1, maxdef = 0):
		if atacado != int(atacado) or atacante != int(atacante):
			return 0
		elif atacado <= maxdef:
			return 1
		elif atacante <= minatk:
			return 0
		elif (atacante, atacado) in CHANCES_GANAR:
			self.ultima_probabilidad =  CHANCES_GANAR[(atacante, atacado)]
			return self.ultima_probabilidad
		else:
			atacantereal = min(atacante, 4)
			atacadoreal = min(atacado, 3)
			chance = CHANCES[(atacantereal, atacadoreal)]
			chancekeys = sorted(chance.keys())
			self.ultima_probabilidad = (chance[chancekeys[0]] * self.ataque(atacante + chancekeys[0][0], atacado + chancekeys[0][1], minatk, maxdef) +
						    chance[chancekeys[1]] * self.ataque(atacante + chancekeys[1][0], atacado + chancekeys[1][1], minatk, maxdef) +
						    chance[chancekeys[2]] * self.ataque(atacante + chancekeys[2][0], atacado + chancekeys[2][1], minatk, maxdef) +
						    chance[chancekeys[3]] * self.ataque(atacante + chancekeys[3][0], atacado + chancekeys[3][1], minatk, maxdef))
			
			return self.ultima_probabilidad
	def ver_ultimo_calculo(self):
		return self.ultima_probabilidad
