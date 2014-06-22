# Aca meto metodos que quiza sirvan quiza no. De tener varios que hacen lo mismo,
# Vemos cual es mas inteligente, o mas rapido, de todos, a ver cual usamos.

Class TachoDeBasura(Jugador):	
	def quiero_atacar(self, tablero, origen, destino): #ATAQUE COMPUESTO
		""" Informa si el pais de destino es una buena opcion para atacar. Recibe
		la probabilidad de exito aceptable y devuelve True si la probabilidad real
		la iguala o supera.
		"""
		# Nombres mas bonitos
		atacante = tablero.ejercitos_pais(origen)
		atacado = tablero.ejercitos_pais(destino)
		if atacante == 1: return False
		# Quiza sea muy obvia la victoria...
		if atacante >= 2*atacado + 1: return True
		
		# En casos mas turbios, usamos el modulo de probas
		if atacante > 1.8*atacado + 1 and (proba.ataque(atacante, atacado) >= 0.7): return True 
		#Use 0.7 xq ya se q mas o menos con doble + 1 siempre superas esa proba.
		# No siempre (Ver 27 vs 13, 31 vs 15) pero muy cerca
		
		# Si el pais solo no puede, buscamos ayuda externa...
		paises_a_componer = [pais for pais in tablero.paises_limitrofes(destino) if self.es_mi_pais(tablero, pais) and pais != origen]
		if not paises_a_componer:
			return False
		
		# Calculamos una probabilidad que no es exacta pero seguro es menor a la exacta.
		atacante += sum([max(tablero.ejercitos_pais(pais)-3,0) for pais in paises_a_componer])
		if atacante >= 2*atacado + 1: return True
		if atacante <= 1.8*atacado + 1: return False
		return (proba.ataque(atacante, atacado) >= 0.7)

	def riesgo_pais(self, tablero, pais):
		'''Devuelve las chances de sobrevivir a un ataque compuesto. (mas o menos)'''
		pass

	def orden_minimo(self, tablero, paises, orden_proteccion):
		""" Dada una lista de paises y un diccionario de orden de proteccion por pais, devuelve
		el orden minimo y una lista de países de ese orden."""
		orden_minimo = min([orden_proteccion[pais] for pais in paises])
		paises_orden_minimo = [pais for pais in paises if orden_proteccion[pais] == orden_minimo]
		return orden_minimo, paises_orden_minimo
		
	def cantidad_de_paises_restantes_para_conquistar_continente_completo(self, tablero, continente)
		""" Calcula la cantidad de paises restantes para conquistar el
		continente completo. Si es totalmente propio, devuelve 0.
		"""
		restantes = 0
		for pais in tablero.paises(continente):
			if not (tablero.color_pais(pais) == self.color):
				restantes += 1
		return restantes
		
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
		# - 
		# - 
		# - 
		
		# Cosas que aumentan los puntos de defensa
		# - Tener menos de 3 ejercitos
		# - No tener aliados
		# - Inferioridad respecto a los enemigos
		# - Inferioridad respecto a los enemigos (Contando aliados)
		# - Que el pais pertenezca a un continente conquistado
		# - 
		# - 
		# - 
		# - 
		ATAQUE = 0
		DEFENSA = 1
		puntajes = {}
		
		for pais in mis_paises_frontera:
			puntajes[pais] = [0, 0]
			# Un pais frontera con menos de 3 ejercitos es un riesgo
			puntajes[pais][DEFENSA] = max(0, 3 - tablero.ejercitos_pais(pais))
			
			limitrofes_aliados = [limitrofe in tablero.paises_limitrofes(pais) if limitrofe in mis_paises_frontera]
			limitrofes_enemigos = [limitrofe in tablero.paises_limitrofes(pais) if tablero.color_pais(limitrofe) != self.color]
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
			
			if (self.cantidad_de_paises_restantes_para_conquistar_continente_completo(tablero, tablero.continente_pais(pais)) \
					< tablero.cantidad_paises_continente()/2):
				puntajes[pais][ATAQUE] += 1
			
			# _/\_ En desarrollo _/\_ 
			
			return puntajes
		
		
	def establecer_prioridades_agregar(self, tablero, paises, ejercitos, continente):
		""" Recibe una lista de paises, una cantidad de ejercitos y un continente
		de limitación (Para disposición libre usar "") y devuelve un diccionario
		con los paises como clave y los ejercitos a agregar como valor. Los paises
		de la lista deben pertenecer al continente y al jugador.
		"""
		# Lista de continentes ordenados por su deseabilidad en forma descendente
		CONTINENTES_ORDENADOS = ["Africa", "Oceania", "America del Sur", "America del Norte", "Europa", "Asia"]
		
		# Solo me interesan los paises propios más expuestos del continente
		orden_proteccion = self.orden_proteccion(tablero)
		orden_minimo, paises_candidatos = self.orden_minimo(tablero, paises, orden_proteccion)
		
		prioridades {}
		if (orden_minimo >= 2):
			# Esta situacion solo es posible si el continente esta totalmente conquistado
			# y no posee ningun pais frontera
			for pais in paises_candidatos:
				prioridades[pais] = ejercitos / len(paises_candidatos)
			for sobrante in xrange(ejercitos % len(paises_candidatos):
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
