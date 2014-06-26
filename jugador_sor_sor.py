import csv
import os

from constantes import *
from jugador import Jugador

# Ejercitos (sin contar el obligatorio) a dejar en paises de orden 2.
EXTRA_ORDEN2 = 1

# Constantes para facil configuracion y correccion
PER_DEFENSOR = 0
PER_CONQUISTADOR = 1
PER_NEUTRAL = 2
PA_NORMAL = 0.49
PA_TARJETA_GANADA = 0.61

class SorSor(Jugador):
	"""
	SorSor, el traidor.
	
	No pertenece a ninguna faccion (ni Alanos ni Barbaros) sino que
	ofrece su espada al mejor postor. Adquirio grandes conocimientos de
	los eruditos de cada bando en paralelo.
	(...Lucas es de la practica Alan y Emiliano de la practica Barbara.)
	No cabe duda que su presencia sera muy determinante pero... ¿Para quien?
	"""
	
	def __init__(self, color, nombre):
		Jugador.__init__(self, color, nombre)
		
		self.ronda = 0
		self.orden_ronda = []

		# Caracteristicas de personalidad
		self.proba_aceptada = 0
		self.caracter = PER_NEUTRAL

		# Inventario
		self.tarjetas = {}
		self.cantidad_canjes = 0

		# Tablero
		self.mis_continentes = []
	
	def ronda_iniciada(self, tablero, ronda, orden_ronda):
		""" Guarda los valores recibidos como parametros, a ser usados por
		el jugador en otras ocasiones.
		"""
		self.ronda = ronda
		self.orden_ronda = orden_ronda
		
	def tarjetas_canjeadas(self, paises):
		""" Esta funcion se llama cada vez que el jugador canjea
		3 tarjetas por ejercitos.
		Agrumentos:
			paises: Lista de paises de las tarjetas canjeadas.
		"""
		for pais in paises:
			self.tarjetas.pop(pais)
		self.cantidad_canjes += 1	
	
	def tarjeta_recibida(self, pais):
		""" Esta funcion se llama cada vez que el jugador recibe una tarjeta.
		"""
		self.tarjetas[pais] = False
		
	def tarjeta_usada(self, pais):
		""" Esta funcion se llama cada vez que el jugador usa una tarjeta
		para incorporar 2 ejercitos en un pais.
		"""
		self.tarjetas[pais] = True
	
	def es_mi_pais(self, tablero, pais):
		""" Devuelve True si el pais indicado es propio."""
		return self.color == tablero.color_pais(pais)
	
	def es_enemigo(self, tablero, pais):
		""" Devuelve True si el pais indicado no es propio."""
		return not self.es_mi_pais(tablero, pais)
	
	def _limita_con(self, tablero, pais, condicion):
		""" Recibe un pais, devuelve True si 
		algun limite cumple con la condicion.
		"""
		for limitrofe in tablero.paises_limitrofes(pais):
			if condicion(tablero, limitrofe):
				return True
		return False
	
	def es_frontera(self, tablero, pais):
		""" Recibe un pais propio, devuelve 
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

	def es_seguro(self, tablero, pais):
		""" Deuvelve True si el pais no puede 
		ser atacado en el siguiente turno.
		"""
		orden_proteccion = self.orden_proteccion(tablero)
		return orden_proteccion[pais] > 3

	def rival_pais(self, tablero, pais):
		"""Devuelve una composicion de los ejercitos
		del mismo color que mas amenazan al pais."""
		return 1 + max((sum((tablero.ejercitos_pais(limitrofe)-1 
						for limitrofe in tablero.paises_limitrofes(pais) 
							if tablero.color_pais(limitrofe) == color)) 
				for color in self.orden_ronda 
					if color != self.color))
		# Indentado en orden de faill lectura (for color if color for limitrofe if tablero...)
	
	def actualizar_personalidad(self, tablero, paises_ganados_ronda=[]):
		""" Usa toda la informacion que puede para determinar el
		caracter de refuerzo ds paises y la
		probabilidad de exito aceptada para afrontar un ataque.
		"""
		if (self.orden_ronda[0] == self.color):
			# Primero en la ronda
			self.caracter = PER_DEFENSOR
		elif (self.orden_ronda[-1] == self.color):
			# Ultimo en la ronda
			self.caracter = PER_CONQUISTADOR
		else:
			# Punto intermedio
			self.caracter = PER_NEUTRAL

		# Lo siguiente se usa solo cuando es llamado por atacar()
		if (len(paises_ganados_ronda) >= 2 or (len(paises_ganados_ronda) == 1 and \
				self.cantidad_canjes < 3)):
			self.proba_aceptada = PA_TARJETA_GANADA
		else:
			self.proba_aceptada = PA_NORMAL
		
		self.mis_continentes = []
		continentes = ('Africa', 'Oceania', 'America del Sur', 'Europa', 'America del Norte', 'Asia')
		for continente in continentes:
			if all((self.es_mi_pais(tablero, pais) for pais in tablero.paises(continente))):
				self.mis_continentes.append(continente)

	@staticmethod
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

	def orden_minimo(self, tablero, paises, orden_proteccion):
		""" Dada una lista de paises y un diccionario de 
		orden de proteccion por pais, devuelveel orden minimo 
		y una lista de paises de ese orden."""
		orden_minimo = min([orden_proteccion[pais] for pais in paises])
		paises_orden_minimo = [pais for pais in paises if orden_proteccion[pais] == orden_minimo]
		return orden_minimo, paises_orden_minimo
		
	
	def atacar(self, tablero, paises_ganados_ronda):
		"""Similar a la del jugador ejemplo"""
		# Actualizar para definir el perfil de ataque
		self.actualizar_personalidad(tablero, paises_ganados_ronda)
		
		mis_paises = (pais for pais in tablero.paises_color(self.color) if tablero.ejercitos_pais(pais) != 1)
		for pais in sorted(mis_paises, key=tablero.ejercitos_pais): # Itera primero los de mas ejercitos
			# Prioriza el limitrofe mas debil.
			for limitrofe in sorted((li for li in tablero.paises_limitrofes(pais) if self.es_enemigo(tablero, li)), key=tablero.ejercitos_pais):
				# Evaluacion de conveniencia usando probabilidades
				if self.quiero_atacar(tablero, pais, limitrofe):
					return pais, limitrofe
		return None
	
	def quiero_atacar(self, tablero, origen, destino):
		""" Informa si el pais de destino es una buena opcion para atacar.
		Esto dependera de muchos factores:
			*Si tenemos suficientes paises para tomar tarjeta
			*Las probabilidades de conquistar el pais enemigo
			*Las probabilidades de hacerlo con ayuda aliada
			*El riesgo en que quedara nuestro pais a ataques enemigos
		"""
		# Probabilidades de conquista tolerada de parte del enemigo en el peor casos
		# de ataque
		PROBA_INVERSA = 0.3
		
		# Ejercitos de paises
		atacante = tablero.ejercitos_pais(origen)
		atacado = tablero.ejercitos_pais(destino)
		if atacante == 1: return False

		# En casos extremos no hace falta usar el modulo de probas
		# Victoria muy probable, con el doble de ejercitos + 1
		if atacante >= 2*atacado + 1:
			return True
		
		# Considera si vale la pena hacer "sangrar" al oponente. Atacara mientras que no se considere en peligro si pierde.
		if (atacante >= atacado and (proba.ataque(self.rival_pais(tablero, origen), atacante-3) < PROBA_INVERSA)):
			return True

		# Para los casos restantes se necesita ayuda externa: Ataque compuesto
		paises_a_componer = [pais for pais in tablero.paises_limitrofes(destino) if self.es_mi_pais(tablero, pais) and pais != origen]
		if not paises_a_componer: return False
		
		# Calculamos una probabilidad que no es exacta pero 
		# seguro es menor a la exacta de ganar con ataque compuesto
		atacante += sum([max(tablero.ejercitos_pais(pais)-3,0) for pais in paises_a_componer])
		if (atacante >= 2*atacado + 1):
			return True
		return (proba.ataque(atacante, atacado) >= self.proba_aceptada)

	def mover(self, origen, destino, tablero, paises_ganados_ronda):
		""" Se ejecuta al ocupar un pais y devuelve la cantidad de ejercitos
		de ocupacion."""

		# Chequeo si hay algun limitrofe del nuevo pais (y no del viejo) con 1 ejercito
		enemigo_facil = [limitrofe for limitrofe in tablero.paises_limitrofes(destino)
					 if tablero.color_pais(limitrofe) != self.color
					 and tablero.ejercitos_pais(limitrofe) == 1
					 and limitrofe not in tablero.paises_limitrofes(origen)]
		if enemigo_facil:
			# Muevo la mayor cantidad de ejercitos posible, evitando que el origen 
			# quede con menos ejercitos que 1+EXTRA_ORDEN2.
			return max(1, min(3, tablero.ejercitos_pais(origen) - EXTRA_ORDEN2 - 1))
		else:
			return 1
			
	def reagrupar(self, tablero, paises_ganados_ronda):
		""" Mueve todos los ejercitos de un pais a paises 
		de orden inferior. En caso de orden 2, se quedara 
		con 3 si puede.
		"""
		reagrupamientos = []
		
		# Lleva la cuenta de los ejercitos disponibles para reagrupar de los
		# paises involucrados en esta ronda (Para evitar el traslado de ejercitos
		# en cadena)
		ejercitos_reagrupables = {pais: (tablero.ejercitos_pais(pais) - 1)
					  for pais in tablero.paises_color(self.color)
					  if tablero.ejercitos_pais(pais) > 1}
					  
		orden_proteccion = self.orden_proteccion(tablero)
		for pais in sorted(ejercitos_reagrupables.keys(), key=lambda pais: orden_proteccion[pais], reverse=True):
			if orden_proteccion[pais] == 1:
				continue
				
			# Defino quienes van a ser los que reciban algo de este pais.
			limitrofes_a_recibir = [limitrofe for limitrofe in tablero.paises_limitrofes(pais) if (
				self.es_mi_pais(tablero, limitrofe) and orden_proteccion[limitrofe] < orden_proteccion[pais])]
				
			# Les reparto a cada uno una cantidad igual de todos mis ejercitos.
			ejercitos_a_enviar = ejercitos_reagrupables[pais]


			# En caso de que el pais sea de orden 2, repartira segun el riesgo del pais
			# pero quedandose con EXTRA_ORDEN2 al final si es posible.
			if orden_proteccion[pais] == 2:
				ejercitos_a_enviar = max(ejercitos_a_enviar - EXTRA_ORDEN2, 0)
				if not ejercitos_a_enviar:
					continue
				agregados = {}
				self._agregar_en_fronteras(tablero, agregados, limitrofes_a_recibir, ejercitos_a_enviar)
				[reagrupamientos.append( (pais, limitrofe, agregados[limitrofe]) ) for limitrofe in agregados]
				continue
			
			for limitrofe in limitrofes_a_recibir:
				ejercitos_reagrupables[pais] -= ejercitos_a_enviar/len(limitrofes_a_recibir)
				reagrupamientos.append( (pais, limitrofe, ejercitos_a_enviar/len(limitrofes_a_recibir)) )

			# Reparto los que sobraron.
			ejercitos_restantes = ejercitos_a_enviar % len(limitrofes_a_recibir)
			if not ejercitos_restantes:
				continue
			for x in xrange(ejercitos_restantes):
				ejercitos_reagrupables[pais] -= 1
				reagrupamientos.append( (pais, limitrofes_a_recibir[x], 1) )
			
		return reagrupamientos
		
	def agregar_ejercitos(self, tablero, cantidad):
		"""Multiples formas de agregar segun la situacion de la partida."""
		if self.ronda == 1:
			return self._agregar_ejercitos_inicial(tablero, cantidad[""])
			
		self.actualizar_personalidad(tablero)
			
		jugada = {}
		# Agregado continental. Son agregados muy defensivos, pero que considero 
		# inevitables aun si uno quiere atacar.
		for continente, cantidad_continente in sorted(cantidad.items(), reverse=True):
			
			# Dejamos el caso de ejercitos libres para otra funcion.
			if continente == '':
				continue

			# Aqui determina para cada continente los paises de minimo orden, donde querrremos nuestros ejercitos
			orden_proteccion = self.orden_proteccion(tablero)
			orden_minimo,paises_orden_minimo = self.orden_minimo(tablero, tablero.paises(continente), orden_proteccion)
			paises_posibles = paises_orden_minimo
			
			ejercitos = cantidad_continente
			
			if orden_minimo == 1:
				self._agregar_en_fronteras(tablero, jugada, paises_posibles, ejercitos)

			else: # Como queremos que agregue si no hay fronteras.
				i = 0
				while ejercitos:
					# Elige el pais de orden minimo con menos ejercitos y le da uno.
					pais_elegido = min(paises_posibles, key=tablero.ejercitos_pais)
					jugada[pais_elegido] = jugada.get(pais_elegido, 0) + 1
					ejercitos -= 1
					i += 1

		self._agregar_ejercitos_libres(tablero, cantidad[''], jugada)
		return jugada
		
	def _agregar_ejercitos_inicial(self, tablero, cantidad):
		"""Agregado inicial de ejercitos. Cantidad sera 5 o 3 en esta modalidad de TEG."""
		precaucion = 1
		continentes = ['Africa', 'Oceania', 'America del Sur', 'Europa', 'America del Norte']
		conquistables, paises_elegidos = self._chequear_continentes_faciles(tablero, precaucion)

		# Este recibe un continente y devuelve una lista de tus paises en el.
		mis_paises_en_ = lambda continente: [pais for pais in tablero.paises(continente) if self.es_mi_pais(tablero, pais)]

		# Agregaremos en el mejor continente que haya pasado las condiciones.
		# para lograrlo, los ordenamos segun el porcentaje de paises que poseemos en el, redondeado ampliamente.
		# (Ej: Si tenemos 3/6 (50%, redondeado a 5) paises en africa y 8/15 (53.3%, redondeado a 5) en asia, agregara en africa)	
		# Si no hay ninguno, agregamos en el pais con mas limites enemigos de ejercito 1 que tengamos.
		if not conquistables: continente = ''
		else: continente = max(conquistables, key=lambda continente:
				       (len(mis_paises_en_(continente))*4/len(tablero.paises(continente))))

		jugada = {}
		top_limitrofes_debiles = self._top_limitrofes_debiles(tablero, precaucion, continente)
		if not top_limitrofes_debiles:
			pais_elegido = [pais for pais in tablero.paises(continente) if self.es_mi_pais(tablero, pais)][0]
		else:
			pais_elegido = top_limitrofes_debiles[0]
		jugada[pais_elegido] = cantidad
		return jugada
	
	def _chequear_continentes_faciles(self, tablero, precaucion):
		""" Devuelve una lista con los continentes conquistables en 1 turno ordenados del mejor al peor."""
		# Esta lista de continentes esta ordenada segun la prioridad (cual conviene mas).
		continentes = ('Africa', 'Oceania', 'America del Sur', 'Europa', 'America del Norte') 
		conquistables = []
		paises_elegidos = []

		# Este recibe un continente y devuelve una lista de tus paises en el.
		mis_paises_en_ = lambda continente: [pais for pais in tablero.paises(continente) if self.es_mi_pais(tablero, pais)]

		# Este recibe uno de mis paises y devuelve una lista con los limitrofes enemigos del mismo continente.
		limitrofes_enemigos = lambda pais: [limitrofe for limitrofe in tablero.paises_limitrofes(pais)
							if limitrofe in tablero.paises(continente)
							and self.es_enemigo(tablero, limitrofe)]

		# Chequea en que continentes tenes 1 pais que puede atacar a todos los que te faltan
		for continente in continentes:
			if len(mis_paises_en_(continente)) == len(tablero.paises(continente)):
				continue
			for pais in mis_paises_en_(continente):
				ejercitos_limitrofes_enemigos = lambda pais: sum([tablero.ejercitos_pais(lim) for lim in limitrofes_enemigos(pais)])
				
				if len(limitrofes_enemigos(pais)) + len(mis_paises_en_(continente)) == len(tablero.paises(continente)) and (
					not ejercitos_limitrofes_enemigos(pais) > precaucion *1.0/len(limitrofes_enemigos(pais))):
					conquistables.append(continente)
					paises_elegidos.append((pais,ejercitos_limitrofes_enemigos(pais)))
					break
			continue
		return conquistables, paises_elegidos
		
	def _top_limitrofes_debiles(self, tablero, precaucion, continente = ''):
		""" Devuelve una lista de todos mis paises del continente 
		ordenados segun la cantidad de paises de ejercito menor
		o igual al criterio enemigos del continente a su alrededor.
		De no seleccionar continente, devolvera todos."""
		mis_paises = [pais for pais in tablero.paises(continente) if self.es_mi_pais(tablero, pais)]
		
		# Ordena la lista mis_paises segun la cantidad de paises 
		# limitrofes enemigos de 1 ejercito, de mayor a menor.
		return sorted(mis_paises, key=lambda pais: len(
			[limitrofe for limitrofe in tablero.paises_limitrofes(pais) if 
			not self.es_mi_pais(tablero, pais) and tablero.ejercitos_pais(limitrofe) <= precaucion and 
			tablero.continente_pais(limitrofe) == continente]), reverse=True)
			
	def _agregar_ejercitos_libres(self, tablero, cantidad, jugada):
		''' Agregara los ejercitos libres. Modifica el diccionario de jugada.'''
		
		# Preliminarmente, reforzara las fronteras continentales.
		if self.caracter == PER_DEFENSOR:
			esta_solo = lambda pais: all((not self.es_mi_pais(tablero, limitrofe) for limitrofe in tablero.paises_limitrofes(pais)))
			es_frontera_continental = lambda pais: all((tablero.continente_pais(lim) == pais for lim in tablero.paises_limitrofes(pais)))
			paises_frontera = [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais)
					   and tablero.continente_pais(pais) in self.mis_continentes and not esta_solo(pais)]
			if not paises_frontera:
				pass

			while cantidad and any( ( pais for pais in paises_frontera if proba.ataque(self.rival_pais(tablero, pais), tablero.ejercitos_pais(pais) > 0.3))):
				  self._agregar_en_fronteras(tablero, jugada, paises_frontera, 1)
				  cantidad -= 1

		if not cantidad: return
		# Si sobran, evalua si algun continente esta capturable y lo ataca.
                conquistables, paises_elegidos = self._chequear_continentes_faciles(tablero, cantidad/2)
		if conquistables:
			pais_elegido = paises_elegidos[0][0]
			ejercitos_enemigos = paises_elegidos[0][1]
			ejercitos_agregados = min(cantidad, 2 * ejercitos_enemigos + 1)
			jugada[pais_elegido] = ejercitos_agregados
			cantidad -= ejercitos_agregados

		if not cantidad: return
		
		# Luego, agregara los sobrantes en paises buscando aumentar sus chances de conquista.
		else:
			limitrofe_mas_debil = lambda pais: min([limitrofe for limitrofe in tablero.paises_limitrofes(pais) if not self.es_mi_pais(tablero, limitrofe)],key=tablero.ejercitos_pais)

			# paises_agregables devuelve todos los paises en los que la probabilidad de atacar al mas debil no sea aceptada.
			paises_agregables = [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais) and
						proba.ataque(tablero.ejercitos_pais(pais), tablero.ejercitos_pais(limitrofe_mas_debil(pais))) < self.proba_aceptada]
			if paises_agregables == []:
				paises_agregables = [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais)]

			while cantidad:
				# El pais elegido sera el que quede con mejor probabilidad luego de agregar.
				pais_elegido = max(paises_agregables, key=lambda pais:
							proba.ataque(tablero.ejercitos_pais(pais) + jugada.get(pais, 0) + 1,
							tablero.ejercitos_pais(limitrofe_mas_debil(pais))))
				jugada[pais_elegido] = jugada.get(pais_elegido, 0) + 1
				cantidad -= 1
	
	def _agregar_en_fronteras(self, tablero, agregados, paises_frontera, ejercitos):
		""" Recibe una lista de paises frontera propios y un 
		diccionario de adiciones previas. Modifica este
		diccionario con los ejercitos agregados en algun
		pais segun el criterio.
		"""
		
		# Este diccionario asigna a cada pais la fuerza (ejercitos compuestos) del enemigo mas poderoso.
		amenaza_mas_poderosa = {pais: self.rival_pais(tablero, pais) for pais in paises_frontera}

		# Devuelve las chances de que el mas poderoso rival conquiste 
		# el pais (considerando los nuevos ejercitos agregados).
		probabilidad_de_morir = lambda pais: proba.ataque(amenaza_mas_poderosa[pais], tablero.ejercitos_pais(pais) + agregados.get(pais, 0))
		pais_elegido = lambda: max(paises_frontera, key=probabilidad_de_morir)
		agregar_a_pais_elegido = lambda: agregados.update([(pais_elegido(), agregados.get(pais_elegido(), 0) + 1)])
		
		# Bucle donde se agregan ejercitos de a uno, revisando en cada iteracion
		# el pais en mayor peligro.
		[agregar_a_pais_elegido() for x in xrange(ejercitos)]
		return
		
# NOTA: TODO LO SIGUIENTE IBA EN OTROS MODULOS, PERO POR EL FORMATO DE ENTREGA HUBO QUE JUNTAR TODO

# Constantes usadas para las probabilidades
CHANCES = {
    (2, 1): {
        (0, -1): 15.0/36,
        (-1, 0): 21.0/36,
        (0.5, 0): 0,
        (0, 0.5): 0,
        },

    (2, 2): {
        (0, -1): 55.0/216,
        (-1, 0): 161.0/216,
        (0.5, 0): 0,
        (0, 0.5): 0,
        },

    (2, 3): {
        (0, -1): 225.0/1296,
        (-1, 0): 1071.0/1296,
        (0.5, 0): 0,
        (0, 0.5): 0,
        },

    (3, 1): {
        (0, -1): 125.0/216,
        (-1, 0): 91.0/216,
        (0.5, 0): 0,
        (0, 0.5): 0,
        },

    (3, 2): {
        (0, -2): 295.0/1296,
        (-1, -1): 420.0/1296,
        (-2, 0): 581.0/1296,
        (0.5, 0): 0,
        },
    
    (3, 3): {
        (0, -2): 979.0/7776,
        (-1, -1): 1981.0/7776,
        (-2, 0): 4816.0/7776,
        (0.5, 0): 0,
        },

    (4, 1): {
        (0, -1): 855.0/1296,
        (-1, 0): 441.0/1296,
        (0.5, 0): 0,
        (0, 0.5): 0,
        },

    (4, 2): {
        (0, -2): 2890.0/7776,
        (-1, -1): 2611.0/7776,
        (-2, 0): 2275.0/7776,
        (0.5, 0): 0,
        },

    (4, 3): {
        (0, -3): 6420.0/46656,
        (-1, -2): 10017.0/46656,
        (-2, -1): 12348.0/46656,
        (-3, 0): 17871.0/46656,
        },
    }
	
# Campos de las bases de datos
ATACANTE = 0
ATACADO = 1
MINATK = 2
MAXDEF = 3
PROBA_BASICA = 2
PROBA_CONDICIONAL = 4

# Funciones de manejo de datos

def desencadenar(valor):
        ''' Recibe una cadena numerica y la convierte a
        int o float, segun si es un numero entero o no,
        respectivamente.
        '''
        try:
                valor = float(valor)
                if valor == int(valor):
                        valor = int(valor)
                return valor
        except:
                raise ValueError("Recibio un valor no numerico!")

def crear_base(nombre_archivo = ".base.csv"):
        ''' Convierte los datos de nuestro archivo de 
        probabilidades calculadas a un diccionario y 
        lo devuelve.
        '''
        if nombre_archivo not in [elem[2] for elem in os.walk(".")]:
        	_flushear_archivo()
        try:
                archivo = open(nombre_archivo, "r")
                archivo_csv = csv.reader(archivo)
        except IOError:
                raise RuntimeError("Error al abrir el archivo de datos")
        try:
                base = {}
                archivo_csv.next()
                for linea in archivo_csv:
                        atacante = desencadenar(linea[ATACANTE])
                        atacado = desencadenar(linea[ATACADO])
                        probabilidad = desencadenar(linea[PROBA_BASICA])
                        if linea: actualizar_base(base, atacante, atacado, probabilidad)
                return base
        except:
                raise RuntimeError("El csv esta todo mal")
        finally:
                archivo.close()

def agregar_proba(nombre_archivo, atacante, atacado, probabilidad, escritura = "a"):
        try:
                archivo = open(nombre_archivo, escritura)
                escritor_csv = csv.writer(archivo)
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        escritor_csv.writerow([atacante, atacado, probabilidad])
        archivo.close()

def actualizar_base(base, atacante, atacado, probabilidad):
        base[(atacante, atacado)] = probabilidad

def crear_base_condicional(nombre_archivo = "base_condicional.csv"):
        ''' Convierte los datos de nuestro archivo de 
        probabilidades calculadas a un diccionario y 
        lo devuelve.
        '''
        if nombre_archivo not in [elem[2] for elem in os.walk(".")]:
        	_flushear_archivo_condicional()
        try:
                archivo = open(nombre_archivo)
                archivo_csv = csv.reader(archivo)
        except IOError:
                raise RuntimeError("Error al abrir el archivo de datos")
		
        try:
                base = {}
                archivo_csv.next()
                for linea in archivo_csv:
                        atacante = desencadenar(linea[ATACANTE])
                        atacado = desencadenar(linea[ATACADO])
                        minatk = desencadenar(linea[MINATK])
                        maxdef = desencadenar(linea[MAXDEF])
                        probabilidad = desencadenar(linea[PROBA_CONDICIONAL])
                        if linea: actualizar_base_condicional(base, atacante, atacado, minatk, maxdef, probabilidad)
                return base
        except:
                raise RuntimeError()
        finally:
                archivo.close()

def agregar_proba_condicional(nombre_archivo, atacante, atacado, minatk, maxdef, probabilidad, escritura = "a"):
        try:
                archivo = open(nombre_archivo, escritura)
                escritor_csv = csv.writer(archivo)
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        escritor_csv.writerow([atacante, atacado, minatk, maxdef, probabilidad])
        archivo.close()

def actualizar_base_condicional(base, atacante, atacado, minatk, maxdef, probabilidad):
        if (atacante, atacado) not in base:
                base[(atacante, atacado)] = {}
        base[(atacante, atacado)].update({(minatk, maxdef): probabilidad})

def _crear_backup(nombre_archivo = ".base_BACKUP.csv"):
        agregar_proba(nombre_archivo, "Atacante", "Atacado", "Probabilidad", "w")

def _crear_backup_condicional(nombre_archivo = ".base_condicional_BACKUP.csv"):
        agregar_proba_condicional(nombre_archivo, "Atacante", "Atacado", "Minatk", "Maxdef", "Probabilidad", "w")

def _flushear_archivo():
        _crear_backup(nombre_archivo = "base.csv")

def _flushear_archivo_condicional():
        _crear_backup_condicional("base_condicional.csv")
		
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
                        atacante + ck[x][0], atacado + ck[x][1], minatk, maxdef) for x in xrange(4)])

		# Aqui, luego de realizar los calculos, agrega a la base de datos los resultados nuevos.
		if minatk == 1 and maxdef == 0:
			self._actualizar_base1(atacante, atacado, self.ultima_probabilidad)
			agregar_proba("base.csv", atacante, atacado, self.ultima_probabilidad)
		else:
			self._actualizar_base2(atacante, atacado, minatk, maxdef, self.ultima_probabilidad)
			agregar_proba_condicional("base_condicional.csv", atacante, atacado, minatk, maxdef, self.ultima_probabilidad)
		
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

	def ver_ultimo_calculo(self):
		""" Devuelve el resultado del ultimo calculo de probabilidad.
		"""
		return self.ultima_probabilidad

# Instancia unica de Probabilidad. Se puede compartir entre jugadores
proba = Probabilidad()

