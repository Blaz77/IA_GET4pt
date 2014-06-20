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
		una lista de países cuyo orden es minimo."""
		orden_minimo = min([orden_proteccion[pais] for pais in paises])
		paises_orden_minimo = [pais for pais in paises if orden_proteccion[pais] == orden_minimo]
		return paises_orden_minimo
		
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
		for continente in sorted(cantidad.keys(), reverse=True)::
			paises_posibles = tablero.paises(continente)
			ejercitos = cantidad[continente]
			while (ejercitos > 0):
				for pais in paises_posibles:
					# Cuidado: Riesgo de bucle infinito
					if (orden_proteccion[pais] > 1 or orden_proteccion[pais] == 1 and \
							self.quiero_agregar(tablero, pais) == True)
						jugada[pais] = jugada.get(pais, 0) + 1
						
						ejercitos -= 1
					if (ejercitos == 0): break
		return jugada
		
	def establecer_prioridades_agregar(self, tablero, paises, ejercitos, continente):
		""" Recibe una lista de paises, una cantidad de ejercitos y un continente
		de limitación (Para disposición libre usar "") y devuelve un diccionario
		con los paises como clave y los ejercitos a agregar como valor. Los paises
		de la lista deben pertenecer al continente.
		"""
		# Solo me interesan los paises propios más expuestos del continente
		orden_proteccion = self.orden_proteccion(tablero)
		paises_candidatos = self.orden_minimo(tablero, paises, orden_proteccion)
		
		prioridades {}
		if (continente != ""):
			# Al definir un continente, se que esta conquistado por completo.
	
	def quiero_agregar(self, tablero, pais_frontera):
		""" Informa si el pais frontera es una buena opcion para agregar ejercitos """
		# Quiero agregar si algun pais vecino es enemigo
		return True
