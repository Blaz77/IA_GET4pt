
from constantes import *
from jugador import Jugador

class JugadorInteligente(Jugador):
	"""
	Este jugador va a ganar el torneo!

	(Escribir codigo de aca para abajo)
	"""

	def _limita_con(self, tablero, pais, condicion):
		""" Recibe un pais, devuelve True si 
		algun limite cumple con la condicion.
		"""
		if not self.es_mi_pais(tablero, pais):
			raise ValueError("No es tu pais!")
		for limitrofe in tablero.paises_limitrofes(pais):
			if condicion(tablero, limitrofe):
				return True
		return False
	
	def es_mi_pais(self, tablero, pais):
		return self.color == tablero.color_pais(pais)
	
	def es_enemigo(self, tablero, pais):
		return not self.es_mi_pais(tablero, pais)
	
	def es_frontera(self, tablero, pais):
		""" Recibe un pais aliado, devuelve 
		True si limita con algun pais enemigo.
		"""
		return self._limita_con(tablero, pais, self.es_enemigo)
	
	def es_amenaza(self, tablero, pais):
		""" Recibe un pais enemigo, devuelve True 
		si limita con alguno de los paises aliados.
		"""
		if es_mi_pais(self, tablero, pais):
			raise ValueError()
		return self.limita_con(tablero, pais, self.es_frontera)
	
	def es_frontera_unica(self, tablero, pais):
		""" Devuelve True si el pais es frontera y 
		no limita con ninguna otra.
		"""
		es_frontera = self.es_frontera(tablero, pais)
		if not es_frontera:
			return False
		return not self._limita_con(tablero, pais, self.es_frontera)
		
	def es_seguro(self, tablero, pais):
		""" Deuvelve True si el pais no puede 
		ser atacado en el siguiente turno.
		"""
		return orden_proteccion[pais] > 3
	
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
		
	def reagrupar(self, tablero, paises_ganados_ronda):
		""" Mueve todos los ejercitos de un pais a paises 
		de orden inferior. En caso de orden 2, se quedara 
		con 3 si puede.
		NO FUNCIONA! No se porque hace levantar error en dados.
		Tal vez estoy pidiendo movimientos ilegales sin darme cuenta...
		"""
		# Ejercitos (sin contar el obligatorio) a dejar en paises de orden 2.
		EXTRA_ORDEN2 = 2
		reagrupamientos = []
		cambios = {}
		orden_proteccion = self.orden_proteccion(tablero)
		orden_a_mover = max(orden_proteccion.values())
		while orden_a_mover >= 2:
			paises_a_mover = [pais for pais in orden_proteccion if orden_proteccion[pais] == orden_a_mover]
			orden_pais = orden_a_mover
			for pais in paises_a_mover:
				# Defino quienes van a ser los que reciban algo de este pais.
				limitrofes_a_recibir = [limitrofe for limitrofe in tablero.paises_limitrofes(pais) if (
					limitrofe in orden_proteccion and orden_proteccion[limitrofe] < orden_pais)]
				
				# Les reparto a cada uno una cantidad igual de todos mis ejercitos.
				ejercitos_a_enviar = tablero.ejercitos_pais(pais) - 1
				# En caso de que el pais sea de orden 2, repartira pero quedandose con EXTRA_ORDEN2 al final si es posible.
				if orden_pais == 2:
					ejercitos_recibidos = sum([x[2] for x in reagrupamientos if x[1] == pais])
					ejercitos_a_enviar -= min(EXTRA_ORDEN2 - ejercitos_recibidos, EXTRA_ORDEN2)
				
				# Para que lo hacemos laburar al pedo, no?
				# Para eso esta la PC, trabaja esclavo!
				if not ejercitos_a_enviar:
					continue
				
				
				for limitrofe in limitrofes_a_recibir:
					reagrupamientos.append( (pais, limitrofe, ejercitos_a_enviar/len(limitrofes_a_recibir)) )
					tablero.actualizar_interfaz(self._cambiar(reagrupamientos, cambios))
				
				# Reparto los que sobraron.	
				# Esto deberia dar un AssertionError, veremos.
				ejercitos_restantes = ejercitos_a_enviar % len(limitrofes_a_recibir)
				if not ejercitos_restantes:
					continue
				for x in range(ejercitos_restantes):
					reagrupamientos.append( (pais, limitrofes_a_recibir[x], 1) )
					tablero.actualizar_interfaz(self._cambiar(reagrupamientos, cambios))
					
			orden_a_mover -= 1
			
		# ACA ME FALTA IMPLEMENTAR QUE UNA FRONTERA LE PASE EJERCITOS A OTRA SI HACE FALTA PARA MAXIMIZAR LA SEGURIDAD.
		return reagrupamientos
