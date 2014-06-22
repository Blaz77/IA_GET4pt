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
			# Agregado defensivo en continentes conquistados
			for continente in self.continentes_conquistados:
				paises_de_interes = [pais for pais in paises_candidatos if tablero.continente_pais(pais) == continente]
				
				# Prioridad maxima: Defender las entradas de los continentes con al menos 3
				# ejercitos
				for pais in paises_candidatos:
					prioridades[pais] = max(0, min(restantes, 3-tablero.ejercitos_pais(pais)))
					restantes -= prioridades[pais]
			
			if (restantes > 0):
				if (self.caracter == PER_CONQUISTADOR):
					# Pongo ejercitos en paises que limitan con otros conquistables
					ejercitos_minimo = 1
					while (restantes == 0):
				elif (self.caracter == PER_DEFENSOR):
					
				elif (self.caracter == PER_NEUTRAL):
					
			return prioridades
