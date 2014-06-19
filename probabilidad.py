from constantes_probabilidad import *
from manejo_datos import crear_base, crear_base_condicional, agregar_proba, agregar_proba_condicional, actualizar_base, actualizar_base_condicional

class Probabilidad(object):
	""" Coleccion de motores de probabilidades teoricas."""
	def __init__(self, ultima_probabilidad = 0):
		self.ultima_probabilidad = ultima_probabilidad
		self.base1 = crear_base()
		self.base2 = crear_base_condicional()
		#Si los archivos son pesados, va a tardar en cargarse, pero solo cargara todos los datos a memoria 1 vez.	
	
	def ataque(self, atacante, atacado, minatk = 1, maxdef = 0):
		""" Devuelve la probabilidad real de reducir
		los ejercitos enemigos a maxdef atacando
		mientras los nuestros no lleguen a minatk.
		ALERTA: Muy lenta en combates grandes no guardados.
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

		# Hay una base de datos para probabilidades con minatk=1 y maxdef=0, y otra para los demas casos.
		if minatk == 1 and maxdef == 0:
			base = self.base1
		else:
			base = self.base2
		
		if (atacante, atacado) in base:
			if minatk == 1 and maxdef == 0:
				self.ultima_probabilidad = base[(atacante, atacado)]
				return self.ultima_probabilidad
			elif (minatk, maxdef) in base[(atacante, atacado)]:
				self.ultima_probabilidad = base[(atacante, atacado)][(minatk, maxdef)]
				return self.ultima_probabilidad

		#-RECURSIVIDAD-
		# En lugar de generarse una pila de datos simple en la PC,
		# se genera una pila con 4 elementos a la par, y a cada uno
		# de esos se le apilan 4 a la par encima, como un "arbol al infinito".
		atacantereal = min(atacante, 4)
		atacadoreal = min(atacado, 3)
		chance = CHANCES[(atacantereal, atacadoreal)]
		ck = sorted(chance.keys())
		self.ultima_probabilidad = sum([chance[ck[x]] * self.ataque(
                        atacante + ck[x][0], atacado + ck[x][1], minatk, maxdef) for x in range(4)])

		# Aqui, luego de realizar los calculos, agrega a la base de datos los resultados nuevos.
		if minatk == 1 and maxdef == 0:
			self._actualizar_base1(atacante, atacado, self.ultima_probabilidad)
			agregar_proba("./bases/base.csv", atacante, atacado, self.ultima_probabilidad)
		else:
			self._actualizar_base2(atacante, atacado, minatk, maxdef, self.ultima_probabilidad)
			agregar_proba_condicional("./bases/base_condicional.csv", atacante, atacado, minatk, maxdef, self.ultima_probabilidad)
		
		# Devuelvo el elemento aqui mismo, quedando igual guardado en el atributo hasta un nuevo calculo.
		return self.ultima_probabilidad
	
	def _actualizar_base1(self, atacante, atacado, probabilidad):
		"""Agrega datos a la base que tenemos cargada en atributos"""
		self.base1[(atacante, atacado)] = probabilidad
	
	def _actualizar_base2(self, atacante, atacado, minatk, maxdef, probabilidad):
		"""Agrega datos a la base condicional que tenemos cargada en atributos"""
		if (atacante, atacado) not in self.base2:
			self.base2[(atacante, atacado)] = {}
		self.base2[(atacante, atacado)].update({(minatk, maxdef): probabilidad})
	
	def ataque_doble(self, atacante, atacado, minatk = 1, maxdef = 0, atk2 = 1, minatk2 = 1):
		"""Calcula la probabilidad de conquistar un pais si lo atacamos de a 2."""
		#NO ESTA TESTEADO! Poco confiable, no usar.
		self.ultima_probabilidad = self.ataque(atacante, atacado, minatk, maxdef)
		for i in range(atacado - maxdef):
			j = i + 1
			self.ultima_probabilidad += (1 - self.ultima_probabilidad) * self.ataque(atk2, atacado, minatk2, maxdef)
		return self.ultima_probabilidad

	def ver_ultimo_calculo(self):
		""" Devuelve el resultado del ultimo calculo de probabilidad.
		"""
		return self.ultima_probabilidad

# Este de aca esta para hacer pruebas en terminal mas rapido, despues lo borro.
proba = Probabilidad()
