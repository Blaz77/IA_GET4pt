
from constantes import *
from jugador import Jugador

class AlejandroSorbello(JugadorInteligente):
	"""
	Mi hermano. Si logramos emularlo sera una 
	fuerza de infinita destruccion y miseria.
	"""

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
