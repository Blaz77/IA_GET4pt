from constantes_probabilidad import *
from manejo_datos import crear_base, crear_base_condicional, agregar_proba, agregar_proba_condicional

class Probabilidad(object):
	""" Coleccion de motores de probabilidades teoricas."""
	def __init__(self, ultima_probabilidad = 0):
		self.ultima_probabilidad = ultima_probabilidad
	
	def ataque(self, atacante, atacado, minatk = 1,
                   maxdef = 0, nombre_archivo = "./bases/base.csv",
                   nombre_archivo2 = "./bases/base_condicional.csv"):
                
		""" Devuelve la probabilidad real de reducir
                los ejercitos enemigos a maxdef atacando
                mientras los nuestros no lleguen a minatk.
                ALERTA: Muy lenta en datos no guardados.
                """
		
		#-BASE-
		# Destruccion de ramas inutiles del "arbol al infinito".
		if atacado != int(atacado) or atacante != int(atacante):
			return 0
		# Detenemos la rama si llegamos al objetivo...
		if atacado <= maxdef:
			return 1
		# ...o si fracasamos.
		if atacante <= minatk:
			return 0
		
		# Hay una base de datos para probabilidades con minatk=0 y maxdef=1, y otra para los demas casos.
		if minatk == 1 and maxdef == 0:
			base = crear_base(nombre_archivo)
			if (atacante, atacado) in base:
				self.ultima_probabilidad = base[(atacante, atacado)]
				return self.ultima_probabilidad
		else:
			base = crear_base_condicional(nombre_archivo2)
			if (atacante, atacado) in base and (minatk, maxdef) in base[(atacante, atacado)]:
				self.ultima_probabilidad = base[(atacante, atacado)][(minatk, maxdef)]
				return self.ultima_probabilidad

		#-RECURSIVIDAD-
		# En lugar de generarse una pila de datos simple en la PC,
		# se genera una pila con 4 elementos a la par, y a cada uno
		# de esos se le apilan 4 a la par encima, como un "arbol al infinito".
		atacantereal = min(atacante, 4)
		atacadoreal = min(atacado, 3)
		chance = CHANCES[(atacantereal, atacadoreal)]
		chancekeys = sorted(chance.keys())
		self.ultima_probabilidad = (chance[chancekeys[0]] * self.ataque(atacante + chancekeys[0][0], atacado + chancekeys[0][1], minatk, maxdef, nombre_archivo, nombre_archivo2) +
					    chance[chancekeys[1]] * self.ataque(atacante + chancekeys[1][0], atacado + chancekeys[1][1], minatk, maxdef, nombre_archivo, nombre_archivo2) +
					    chance[chancekeys[2]] * self.ataque(atacante + chancekeys[2][0], atacado + chancekeys[2][1], minatk, maxdef, nombre_archivo, nombre_archivo2) +
					    chance[chancekeys[3]] * self.ataque(atacante + chancekeys[3][0], atacado + chancekeys[3][1], minatk, maxdef, nombre_archivo, nombre_archivo2))

		#Aqui, luego de realizar los calculos, agrega a la base de datos los resultados nuevos.
		if minatk == 1 and maxdef == 0:
			agregar_proba(nombre_archivo, atacante, atacado, self.ultima_probabilidad)
		else:
			agregar_proba_condicional(nombre_archivo2, atacante, atacado, minatk, maxdef, self.ultima_probabilidad)
		
		#Devuelvo el elemento aqui mismo, quedando igual guardado en el atributo hasta un nuevo calculo.
		return self.ultima_probabilidad
		
	def ver_ultimo_calculo(self):
		"""Devuelve el resultado del ultimo calculo de probabilidad.
		"""
		return self.ultima_probabilidad

#Este de aca esta para hacer pruebas en terminal mas rapido, despues lo borro.
proba = Probabilidad()

