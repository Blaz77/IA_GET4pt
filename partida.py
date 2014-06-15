from constantes import *

from jugador_ejemplo import JugadorSuicida, JugadorOfensivo
from jugador_inteligente import JugadorInteligente

#
# Configuracion de jugadores para la partida.
# Cuidado de no repetir colores.
#
jugadores = [
	JugadorSuicida(COLOR_NEGRO, 'Jugador 1'),
	JugadorOfensivo(COLOR_AZUL, 'Jugador 2'),
	JugadorSuicida(COLOR_ROJO, 'Jugador 3'),
	JugadorSuicida(COLOR_ROSA, 'Jugador 4'),
]

