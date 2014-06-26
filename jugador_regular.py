from constantes import *
from jugador import Jugador
from jugador_inteligente import JugadorInteligente
from probabilidad import proba

# Ejercitos (sin contar el obligatorio) a dejar en paises de orden 2.
EXTRA_ORDEN2 = 2

# Constantes para facil configuracion y correccion
PER_DEFENSOR = 0
PER_CONQUISTADOR = 1
PER_NEUTRAL = 2
PA_NORMAL = 0.49
PA_TARJETA_GANADA = 0.61
		
class JugadorRegular(JugadorInteligente):
	""" Tercer prototipo de un jugador inteligente.
	"""
	def __init__(self, color, nombre):
		JugadorInteligente.__init__(self, color, nombre)
		
		self.ronda = 0
		self.orden_ronda = []

		# Caracteristicas de personalidad
		self.proba_aceptada = 0
		self.caracter = PER_NEUTRAL

		# Inventario
		self.tarjetas = {}
		self.cantidad_canjes = 0
	
	def ronda_iniciada(self, tablero, ronda, orden_ronda):
		""" Guarda los valores recibidos como parametros, a ser usados por
		el jugador en otras ocasiones.
		"""
		self.ronda = ronda
		self.orden_ronda = orden_ronda

	def tarjeta_usada(self, pais):
		""" Esta funcion se llama cada vez que el jugador usa una tarjeta
		para incorporar 2 ejercitos en un pais.
		"""
		# Este chequeo sera inutil una vez q confirmemos que nunca ocurre.
		if pais not in self.tarjetas:
			raise ValueError("No la teniamos")
		self.tarjetas[pais] = True

	def tarjeta_recibida(self, pais):
		""" Esta funcion se llama cada vez que el jugador recibe una tarjeta.
		"""
		# Este chequeo sera inutil una vez q confirmemos que nunca ocurre.
		if pais in self.tarjetas:
			raise ValueError("Ya la teniamos")
		self.tarjetas[pais] = False

	def tarjetas_canjeadas(self, paises):
		""" Esta funcion se llama cada vez que el jugador canjea
		3 tarjetas por ejercitos.

		Agrumentos:
			paises: Lista de paises de las tarjetas canjeadas.
		"""
		for pais in paises:
			self.tarjetas.pop(pais)
		self.cantidad_canjes += 1		
	
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
	
	def agregar_ejercitos(self, tablero, cantidad):
		""" . """
		if self.ronda == 1:
			return self._agregar_ejercitos_inicial(tablero, cantidad[""])
			
		self.actualizar_personalidad(tablero)
			
		jugada = {}
		# a continuacion agregados muy defensivos, pero que considero inevitables aun si uno quiere atacar.
		for continente, cantidad_continente in sorted(cantidad.items(), reverse=True):
			
			# Dejamos el caso de ejercitos libres para otra funcion.
			if continente == '':
				continue

			# Aqui determina para cada continente los paises de minimo orden, donde querrremos nuestros ejercitos
			# (Pivote -pais de comunicacion entre fronteras- no implementado aun)
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

	def _agregar_ejercitos_inicial(self, tablero, cantidad):
		"""Agregado inicial de ejercitos. Cantidad sera 5 o 3 en esta modalidad de TEG."""
		precaucion = cantidad/2 + 1
		conquistables = self._chequear_continentes_faciles(tablero, precaucion)
		

		# Este recibe un continente y devuelve una lista de tus paises en el.
		mis_paises_en_ = lambda continente: [pais for pais in tablero.paises(continente) if self.es_mi_pais(tablero, pais)]

		# Agregaremos en el mejor continente que haya pasado las condiciones.
		# para lograrlo, los ordenamos segun el porcentaje de paises que poseemos en el, redondeado ampliamente.
		# (Ej: Si tenemos 3/6 (50%, redondeado a 5) paises en africa y 8/15 (53.3%, redondeado a 5) en asia, agregara en africa)	
		# Si no hay ninguno, agregamos en el pais con mas limites enemigos de ejercito 1 que tengamos.
		if not conquistables: continente = ''
		else: continente = max(conquistables, key=lambda continente:
				       len(mis_paises_en_(continente))*5/len(tablero.paises(continente)))

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
		continentes = ['Africa', 'Oceania', 'America del Sur', 'Europa', 'America del Norte', 'Asia'] 
		conquistables = []

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
				if len(limitrofes_enemigos(pais)) + len(mis_paises_en_(continente)) == len(tablero.paises(continente)) and not(
							[lim for lim in limitrofes_enemigos(pais) if tablero.ejercitos_pais(lim) > precaucion]):
					conquistables.append(continente)
					break
			continue
		return conquistables

                
	def _agregar_ejercitos_libres(self, tablero, cantidad, jugada):
		''' Agregara los ejercitos libres. Modifica el diccionario de jugada.'''
		if self.caracter == PER_DEFENSOR:
			esta_solo = lambda pais: all((not self.es_mi_pais(tablero, limitrofe) for limitrofe in tablero.paises_limitrofes(pais)))
			paises_frontera = [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais) and not esta_solo(pais)]
			if not paises_frontera:
				paises_frontera = [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais)]
			self._agregar_en_fronteras(tablero, jugada, paises_frontera, cantidad)
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
							proba.ataque(tablero.ejercitos_pais(pais) + jugada.get(pais, 0),
							1 + tablero.ejercitos_pais(limitrofe_mas_debil(pais))))
				jugada[pais_elegido] = jugada.get(pais_elegido, 0) + 1
				cantidad -= 1

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

	def atacar(self, tablero, paises_ganados_ronda):
		"""Similar a la del jugador ejemplo"""
		# Actualizar para definir el perfil de ataque
		self.actualizar_personalidad(tablero, paises_ganados_ronda)
		
		mis_paises = (pais for pais in tablero.paises_color(self.color) if tablero.ejercitos_pais(pais) != 1)
		for pais in sorted(mis_paises, key=tablero.ejercitos_pais):
			for limitrofe in sorted((li for li in tablero.paises_limitrofes(pais) if self.es_enemigo(tablero, li)), key=tablero.ejercitos_pais):
				# Evaluacion de conveniencia usando probabilidades
				if self.quiero_atacar(tablero, pais, limitrofe):
					return pais, limitrofe
		return None
	
	def quiero_atacar(self, tablero, origen, destino):
		""" Informa si el pais de destino es una buena opcion para atacar.
		Esto dependera de muchos factores:
			Si tenemos suficientes paises para agarrar tarjeta
			Las probabilidades de conquistar el pais enemigo
			Las probabilidades de hacerlo con ayuda aliada
			El riesgo en que quedara nuestro pais a ataques enemigos
			
		"""
		# Ejercitos de paises
		atacante = tablero.ejercitos_pais(origen)
		atacado = tablero.ejercitos_pais(destino)
		if atacante == 1: return False

		# En casos extremos no hace falta usar el modulo de probas
		# Victoria muy probable, con el doble de ejercitos + 1
		if atacante >= 2*atacado + 1:
			return True

		if (atacante >= atacado and (proba.ataque(self.rival_pais(tablero, origen), atacante-3) < 0.3)):
			return True

		# Para los casos restantes se necesita ayuda externa
		paises_a_componer = [pais for pais in tablero.paises_limitrofes(destino) if self.es_mi_pais(tablero, pais) and pais != origen]
		if not paises_a_componer: return False
		
		# Calculamos una probabilidad que no es exacta pero seguro es menor a la exacta.
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
