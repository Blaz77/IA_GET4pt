# Practicando implementaciones de jugador
# Deberia ganarle a JugadorInexperto
# Mejoras deseadas:
# - Su agresividad se adapta a la situacion
# - No agrega ejercitos en bloque, los reparte
# - Al repartir ejercitos, puede tener varios frentes de batalla
# - Usa las probabilidades para atacar con varios paises contra uno
#   (Ni idea de como vamos a hacer eso)

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
PA_TARJETA_GANADA = 0.67
		
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
			#for color in self.orden_ronda[self.orden_ronda.index(self.color)::]:
			#	amenazas_del_color = [pais for pais in tablero.paises_color(color) if self.es_amenaza(tablero, pais)]
			#	for pais in amenazas_del_color:
			
			# Primero en la ronda
			self.caracter = PER_DEFENSOR
		elif (self.orden_ronda[-1] == self.color):
			# Ultimo en la ronda
			self.caracter = PER_CONQUISTADOR
		else:
			# Punto intermedio
			self.caracter = PER_NEUTRAL
		
		if not paises_ganados_ronda: return
		
		# Lo siguiente se usa solo cuando es llamado por atacar()
		if (len(paises_ganados_ronda) >= 2 or (len(paises_ganados_ronda) == 1 and \
				self.cantidad_canjes < 3)):
			self.proba_aceptada = PA_TARJETA_GANADA
		else:
			self.proba_aceptada = PA_NORMAL
	
	def agregar_ejercitos(self, tablero, cantidad):
		""" Algo de documentacion asi se ve verde y bonito. """
		if self.ronda == 1:
			return self._agregar_ejercitos_inicial(tablero, cantidad[""])
			
		self.actualizar_personalidad(tablero)
			
		jugada = {}
		# a continuacion agregados muy defensivos, pero que considero inevitables aun si uno quiere atacar.
		for continente, cantidad_continente in sorted(cantidad.items(), reverse=True):
			
			# Dejamos el caso de ejercitos libres para otra funcion.
			if continente == '':
				continue
			# Con el fin de agilizar una partida, atontar el jugador si ya gana seguro (poca confianza le tengo)
			if self.victoria_segura(tablero):
				pais_max = max(tablero.paises(continente), key=tablero.ejercitos_pais)
				jugada[pais_max] = jugada.get(pais_max,0) + cantidad_continente
				continue
			
			# Aqui determina para cada continente los paises de minimo orden, donde querrremos nuestros ejercitos
			# (Pivote -pais de comunicacion entre fronteras- no implementado aun)
			orden_proteccion = self.orden_proteccion(tablero)
			orden_minimo,paises_orden_minimo = self.orden_minimo(tablero, tablero.paises(continente), orden_proteccion)
			paises_posibles = paises_orden_minimo
			
			
			ejercitos = cantidad_continente
			i = 0 # Contador para ubicar ejercitos de manera cíclica.
			if orden_minimo == 1: #Como queremos que agrupe en cualquier continente con fronteras
			
				while ejercitos:
					# Este lambda determina para cada pais el ejercito enemigo mas fuerte que lo puede atacar.
					ejercito_mas_poderoso = max([tablero.ejercitos_pais(limitrofe) for limitrofe in
								  tablero.paises_limitrofes(paises_posibles[i%len(paises_posibles)])
								  if self.es_enemigo(tablero, limitrofe) and self.es_amenaza(tablero, limitrofe)])
					
					# Elegiremos entonces agregar un ejercito en la frontera mas amenazada (No contempla ataque compuesto)
					probabilidad_de_morir = lambda pais: proba.ataque(ejercito_mas_poderoso,tablero.ejercitos_pais(pais))
					pais_elegido = max(paises_posibles, key=probabilidad_de_morir)
					jugada[pais_elegido] = jugada.get(pais_elegido, 0) + 1
					ejercitos -= 1
					i += 1
					
			else: # Como queremos que agregue si no hay fronteras.
			
				while ejercitos:
					# Elige el pais de orden minimo con menos ejercitos y le da uno.
					pais_elegido = min(paises_posibles, key=tablero.ejercitos_pais)
					jugada[pais_elegido] = jugada.get(pais_elegido, 0) + 1
					ejercitos -= 1
					i += 1

		self._agregar_ejercitos_libres(tablero, cantidad[''], jugada)
		return jugada
		
	def _agregar_ejercitos_inicial(self, tablero, cantidad):
		"""Cantidad sera 5 o 3 en el modo clasico."""
		
		# Esta lista de continentes esta ordenada segun la prioridad (cual conviene mas).
		continentes = ['Africa', 'Oceania', 'America del Sur', 'Europa', 'America del Norte', 'Asia'] 
		conquistables = list(continentes)
		
		# Numero de ejercitos permitidos que pueden tener los rivales del continente.
		if cantidad == 3:
			precaucion = 2
		else:			
			precaucion = 1
		
		for continente in continentes:
			# Chequea si un continente puede ser conquistado en 1 turno.
			for pais in tablero.paises(continente):
				es_mi_pais = self.es_mi_pais(tablero, pais)
				esta_defendido = tablero.ejercitos_pais(pais) > precaucion
				if not (es_mi_pais or (self.es_amenaza(tablero, pais) and not esta_defendido)):
					conquistables.pop(conquistables.index(continente))
		
		# Agregaremos en el mejor continente que haya pasado las condiciones. 
		# Si no hay ninguno, agregamos en el país con mas limites enemigos de ejercito 1 que tengamos.
		if not conquistables:
			continente = ''
		else:
			continente = conquistables[0]
		jugada = {}
		jugada[self._top_limitrofes_debiles(tablero, continente)[0]] = cantidad
		return jugada

	def _agregar_ejercitos_libres(self, tablero, cantidad, jugada):
		'''Agregara los ejercitos libres'''
		if self.victoria_segura(tablero):
			pais_max = max(tablero.paises_color(self.color), key=tablero.ejercitos_pais)
			jugada[pais_max] = jugada.get(pais_max,0) + cantidad
			return

		if True: #self.caracter == PE_CONQUISTADOR (esto deberia hacerlo solo si quiere atacar: Asi no agrega ejercitos previniendo un agregado ofensivo del rival.
			limitrofe_mas_debil = lambda pais: min([limitrofe for limitrofe in tablero.paises_limitrofes(pais) if not self.es_mi_pais(tablero, limitrofe)],key=tablero.ejercitos_pais)
			# paises_agregables devuelve todos los paises en los que la probabilidad de atacar al mas debil no sea aceptada.
			paises_agregables = [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais) and
					     proba.ataque(tablero.ejercitos_pais(pais), tablero.ejercitos_pais(limitrofe_mas_debil(pais))) < self.proba_aceptada]
			if paises_agregables == []:
				paises_agregables == [pais for pais in tablero.paises_color(self.color) if self.es_frontera(tablero, pais)]

			if paises_agregables == []:
				paises_agregables == tablero.paises_color(self.color)

			while cantidad:
				pais_elegido = max(paises_agregables, key=lambda pais: proba.ataque(tablero.ejercitos_pais(pais), tablero.ejercitos_pais(
					limitrofe_mas_debil(pais))))
				jugada[pais_elegido] = jugada.get(pais_elegido, 0) + 1
				cantidad -= 1

	def _top_limitrofes_debiles(self, tablero, continente = ''):
		'''Devuelve una lista de todos mis paises del continente 
		ordenados segun la cantidad de paises de ejercito 1 enemigos 
		del continente a su alrededor. De no seleccionar continente, 
		devolvera todos.'''
		mis_paises = [pais for pais in tablero.paises(continente) if self.es_mi_pais(tablero, pais)]
		
		# Ordena la lista mis_paises segun la cantidad de paises 
		# limitrofes enemigos de 1 ejercito, de mayor a menor.
		return sorted(mis_paises, key=lambda pais: len(
			[limitrofe for limitrofe in tablero.paises_limitrofes(pais) if 
			not self.es_mi_pais(tablero, pais) and tablero.ejercitos_pais(pais) == 1 and 
			tablero.continente_pais(limitrofe) == continente]), reverse=True)
			
	def agregar_ejercitos(self, tablero, cantidad):
                """ Errores: Es lento como la puta madre y
                agrega repartido en las fronteras.
                La re caga al principio de la partida y no
                prioriza fronteras en peligro.
                """
		jugada = {}
		for continente in sorted(cantidad.keys(), reverse=True):
			paises_posibles = [pais for pais in tablero.paises(continente) if tablero.color_pais(pais) == self.color]
			ejercitos = cantidad[continente]
			jugada_parcial = self.establecer_prioridades_agregar(tablero, paises_posibles, ejercitos, nontinente)
			for pais in jugada_parcial:
				jugada[pais] = jugada.get(pais, 0) + jugada_parcial[pais]
		return jugada
		
	def ponderar_fronteras(self, tablero, mis_paises_frontera):
		""" Genera un diccionario con los paises propios como valor y una lista con
		los puntos de ataque y defensa del mismo. A mayores puntos de ataque, mejor es
		para conquistar paises, y a mayores puntos de defensa, mas critico es su estado
		y mayor necesidad de refuerzos tiene para sobrevivir.
		(Yu-Gi-Teg)
		"""
		# Cosas que aumentan los puntos de ataque:
		# - Paises limitrofes enemigos con menos de 3 ejercitos
		# - Superioridad de ejercitos respecto al total de enemigos
		# - Que pertenezca a un continente casi conquistado
		# - 
		
		# Cosas que aumentan los puntos de defensa
		# - Tener menos de 3 ejercitos
		# - No tener aliados
		# - Inferioridad respecto a los enemigos
		# - Inferioridad respecto a los enemigos (Contando aliados)
		# - Que el pais pertenezca a un continente conquistado
		# - 
		ATAQUE = 0
		DEFENSA = 1
		puntajes = {}
		
		for pais in mis_paises_frontera:
			puntajes[pais] = [0, 0]
			# Un pais frontera con menos de 3 ejercitos es un riesgo
			puntajes[pais][DEFENSA] = max(0, 3 - tablero.ejercitos_pais(pais))
			
			limitrofes_aliados = [limitrofe for limitrofe in tablero.paises_limitrofes(pais) if limitrofe in mis_paises_frontera]
			limitrofes_enemigos = [limitrofe for limitrofe in tablero.paises_limitrofes(pais) if tablero.color_pais(limitrofe) != self.color]
			if (len(limitrofes_aliados == 0)):
				puntajes[pais][DEFENSA] += 1
			
			ejercitos_enemigos = sum(tablero.ejercitos_pais(limitrofe) for limitrofe in limitrofes_enemigos)
			ejercitos_aliados = sum(tablero.ejercitos_pais(limitrofe) for limitrofe in limitrofes_aliados)
			if (ejercitos_enemigos > tablero.ejercitos_pais(pais)): 
				puntajes[pais][DEFENSA] += 1
			else:
				puntajes[pais][ATAQUE] += 1
			if (ejercitos_enemigos > ejercitos_aliados + tablero.ejercitos_pais(pais)): puntajes[pais][DEFENSA] += 1
			
			for limitrofe_enemigo in limitrofes_enemigos:
				if (tablero.ejercitos_pais(limitrofe_enemigo) < 3):
					puntajes[pais][ATAQUE] += 1
			
			if (tablero.continente_pais(pais) in self.continentes_conquistados):
				puntajes[pais][DEFENSA] += 1
			
			if (self.cantidad_paises_restantes_para_conquistar_continente(tablero, tablero.continente_pais(pais)) \
					< tablero.cantidad_paises_continente()/2):
				puntajes[pais][ATAQUE] += 1
			
			# Agregar mas criterios
			
			return puntajes
			
	def establecer_prioridades_agregar(self, tablero, paises, ejercitos, continente):
		""" Recibe una lista de paises, una cantidad de ejercitos y un continente
		de limitación (Para disposición libre usar "") y devuelve un diccionario
		con los paises como clave y los ejercitos a agregar como valor. Los paises
		de la lista deben pertenecer al continente y al jugador.
		"""
		# Solo me interesan los paises propios más expuestos del continente
		orden_proteccion = self.orden_proteccion(tablero)
		orden_minimo, paises_candidatos = self.orden_minimo(tablero, paises, orden_proteccion)
		
		prioridades = {}
		if (orden_minimo >= 2):
			# Esta situacion solo es posible si el continente esta totalmente conquistado
			# y no posee ningun pais frontera
			for pais in paises_candidatos:
				prioridades[pais] = ejercitos / len(paises_candidatos)
			for sobrante in xrange(ejercitos % len(paises_candidatos)):
				prioridades[paises_candidatos[sobrante]] += 1
			return prioridades
		elif (continente != ""):
			# Reforzando paises frontera de continente conquistado
			restantes = ejercitos
			# Prioridad maxima: Defender las entradas de los continentes con al menos 3
			# ejercitos
			for pais in paises_candidatos:
				prioridades[pais] = max(0, min(restantes, 3-tablero.ejercitos_pais(pais)))
				restantes -= prioridades[pais]
			# Si quedan ejercitos, reforzar en paises mas amenazados
			if (restantes > 0):
				amenazas = {}
				for pais in paises_candidatos:
					# Diferencia entre los ejercitos enemigos amenazando al pais y los que posee
					amenazas[pais] = sum([tablero.ejercitos_pais(limitrofe) for limitrofe in tablero.paises_limitrofes(pais) \
							if tablero.color_pais(limitrofe) != self.color]) - (tablero.ejercitos_pais(pais) + prioridades.get(pais, 0))
				# Primero en paises con inferioridad numerica
				paises_de_interes = [pais for pais in amenazas if amenazas[pais] > 0]
				for pais in paises_de_interes:
					ejercitos_agregar = min(restantes, amenazas[pais])
					prioridades[pais] = prioridades.get(pais, 0) + ejercitos_agregar
					restantes -= ejercitos_agregar
					if (restantes == 0): return prioridades
				
				# Luego en paises con igualdad numerica
				paises_de_interes = [pais for pais in amenazas if amenazas[pais] == 0]
				for pais in paises_de_interes:
					prioridades[pais] = prioridades.get(pais, 0) + 1
					restantes -= 1
					if (restantes == 0): return prioridades
		
				# Por ultimo en paises con superioridad numerica
				paises_de_interes = [pais for pais in amenazas if amenazas[pais] < 0]
				while (restantes > 0):
					for pais in paises_de_interes:
						prioridades[pais] = prioridades.get(pais, 0) + 1
						restantes -= 1
						if (restantes == 0): return prioridades
		else:
			restantes = ejercitos
			# Eleccion libre. Solo tengo paises frontera
			puntajes = self.ponderar_fronteras(tablero, paises_candidatos)
			if (self.caracter == PER_CONQUISTADOR):
				total = sum(puntos[ATAQUE] for puntos in puntajes.values())
			elif (self.caracter == PER_DEFENSOR):
				total = sum(puntos[DEFENSA] for puntos in puntajes.values())
			elif (self.caracter == PER_NEUTRAL):
				total = sum(puntos[ATAQUE] + puntos[DEFENSA] for puntos in puntajes.values())
			else: raise ValueError()
			
			# Si tengo 10 ejercitos y el puntaje total es 100, agrego 0.1 ejercitos por punto
			unidad_asignacion = total / float(ejercitos)
			for pais in paises_candidatos:
				if (self.caracter == PER_CONQUISTADOR):
					ejercitos_agregar = int(round(unidad_asignacion * puntajes[pais][ATAQUE]))
				elif (self.caracter == PER_DEFENSOR):
					ejercitos_agregar = int(round(unidad_asignacion * puntajes[pais][DEFENSA]))
				elif (self.caracter == PER_NEUTRAL):
					ejercitos_agregar = int(round(unidad_asignacion * (puntajes[pais][ATAQUE] + puntajes[pais][DEFENSA])))
				
				if (ejercitos_agregar != 0):
					prioridades[pais] = ejercitos_agregar
					restantes -= ejercitos_agregar
			
			assert(restantes == 0)
			
			return prioridades
	
	def cantidad_paises_restantes_para_conquistar_continente(self, tablero, continente):
		""" Calcula la cantidad de paises restantes para conquistar el
		continente completo. Si es totalmente propio, devuelve 0.
		"""
		restantes = 0
		for pais in tablero.paises(continente):
			if not (tablero.color_pais(pais) == self.color):
				restantes += 1
		return restantes
	
	def atacar(self, tablero, paises_ganados_ronda):
		self.actualizar_personalidad(tablero, paises_ganados_ronda)
		
		mis_paises = tablero.paises_color(self.color)
		for pais in mis_paises:
			for limitrofe in tablero.paises_limitrofes(pais):
				# no me quiero atacar a mi mismo
				if tablero.color_pais(limitrofe) == self.color:
					continue
				# Estrenando las probabilidades
				if self.quiero_atacar(tablero, pais, limitrofe):
					return pais, limitrofe
		return None
	
	def quiero_atacar(self, tablero, origen, destino):
		""" Informa si el pais de destino es una buena opcion para atacar. Recibe
		la probabilidad de exito aceptable y devuelve True si la probabilidad real
		la iguala o supera.
		"""
		# Ejercitos de paises
		atacante = tablero.ejercitos_pais(origen)
		atacado = tablero.ejercitos_pais(destino)
		if atacante == 1: return False
		
		# En casos extremos no hace falta usar el modulo de probas
		# Victoria muy probable, con el doble de ejercitos + 1
		if (atacante >= 2*atacado + 1 and self.proba_aceptada <= 0.67): 
			return True
		# Para ataques individuales las probabilidades de ganar con menos ejercitos
		# que el oponente es menor que 0.15
		if (atacante >= atacado and proba.ataque(atacante, atacado) >= self.proba_aceptada):
			return True
			
		# Para los casos restantes se necesita ayuda externa
		paises_a_componer = [pais for pais in tablero.paises_limitrofes(destino) if self.es_mi_pais(tablero, pais) and pais != origen]
		if not paises_a_componer:
			return False
		
		# Importante: Hay que ver el minatk de cada pais, ya que tampoco hay que desprotegerlos
		# Calculamos una probabilidad que no es exacta pero seguro es menor a la exacta.
		atacante += sum([max(tablero.ejercitos_pais(pais)-3,0) for pais in paises_a_componer])
		if (atacante >= 2*atacado + 1 and self.proba_aceptada <= 0.67): return True
		if (atacante < atacado): return False
		return (proba.ataque(atacante, atacado) >= proba_aceptada)

	def mover(self, origen, destino, tablero, paises_ganados_ronda):
		""" Se ejecuta al ocupar un pais y devuelve la cantidad de ejercitos
		de ocupacion."""
		# Muevo la mayor cantidad de ejercitos posible, evitando que el origen 
		# quede con menos ejercitos que 1+EXTRA_ORDEN2.
		return max(1, min(3, tablero.ejercitos_pais(origen) - EXTRA_ORDEN2 - 1))
	
	def reagrupar(self, tablero, paises_ganados_ronda):
		""" Mueve todos los ejercitos de un pais a paises 
		de orden inferior. En caso de orden 2, se quedara 
		con 3 si puede.
		"""
		reagrupamientos = []
		
		# Lleva la cuenta de los ejercitos disponibles para reagrupar de los
		# paises involucrados en esta ronda (Para evitar el traslado de ejercitos
		# en cadena)
		ejercitos_reagrupables = {}
		for pais in tablero.paises_color(self.color):
			if tablero.ejercitos_pais(pais) > 1:
				ejercitos_reagrupables[pais] = tablero.ejercitos_pais(pais) - 1
				
		orden_proteccion = self.orden_proteccion(tablero)
		for pais in ejercitos_reagrupables:
			if orden_proteccion[pais] == 1:
				continue
			# Defino quienes van a ser los que reciban algo de este pais.
			limitrofes_a_recibir = [limitrofe for limitrofe in tablero.paises_limitrofes(pais) if (
				self.es_mi_pais(tablero, limitrofe) and orden_proteccion[limitrofe] < orden_proteccion[pais])]
				
			# Les reparto a cada uno una cantidad igual de todos mis ejercitos.
			ejercitos_a_enviar = ejercitos_reagrupables[pais]
			
			# En caso de que el pais sea de orden 2, repartira pero quedandose con EXTRA_ORDEN2 al final si es posible.
			if orden_proteccion[pais] == 2:
				ejercitos_a_enviar = max(ejercitos_a_enviar - EXTRA_ORDEN2, 0)
				if not ejercitos_a_enviar:
					continue

			for limitrofe in limitrofes_a_recibir:
				ejercitos_reagrupables[pais] -= ejercitos_a_enviar/len(limitrofes_a_recibir)
				reagrupamientos.append( (pais, limitrofe, ejercitos_a_enviar/len(limitrofes_a_recibir)) )
				tablero.actualizar_interfaz(self.cambios(reagrupamientos))

			# Reparto los que sobraron.
			ejercitos_restantes = ejercitos_a_enviar % len(limitrofes_a_recibir)
			if not ejercitos_restantes:
				continue
			for x in xrange(ejercitos_restantes):
				ejercitos_reagrupables[pais] -= 1
				reagrupamientos.append( (pais, limitrofes_a_recibir[x], 1) )
				tablero.actualizar_interfaz(self.cambios(reagrupamientos))
			
		# ACA ME FALTA IMPLEMENTAR QUE UNA FRONTERA LE PASE EJERCITOS A OTRA SI HACE FALTA PARA MAXIMIZAR LA SEGURIDAD.
		return reagrupamientos
