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

	def orden_minimo(self, tablero, continente, orden_proteccion):
		"""Devuelve el minimo orden en un continente y los paises con el mismo."""
		paises_continente_mios = [pais for pais in orden_proteccion if pais in tablero.paises(continente)]
		orden_minimo = min([orden_proteccion[pais] for pais in paises_continente_mios])
		paises = [pais for pais in paises_continente_mios if orden_proteccion[pais] == orden_minimo]
		return paises
		
	def agregar_ejercitos(self, tablero, cantidad):
                """ Errores: Es lento como la puta madre y
                agrega repartido en las fronteras.
                La re caga al principio de la partida y no
                prioriza fronteras en peligro.
                """
		jugada = {}
		orden_proteccion = self.orden_proteccion(tablero)
		for continente in cantidad:
			paises_posibles = self.orden_minimo(tablero, continente, orden_proteccion)
			ejercitos = cantidad[continente]
			while True:
				if not ejercitos:
					break
				for pais in paises_posibles:
					if ejercitos:
						jugada[pais] = jugada.get(pais, 0) + 1
						
						ejercitos -= 1
					else:
						break
		return jugada
