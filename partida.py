from constantes import *

from jugador_ejemplo import JugadorSuicida, JugadorOfensivo
from jugador_inteligente import JugadorInteligente
from jugador_tramposo import JugadorTramposo
from jugador_aprendiz import JugadorAprendiz
from jugador_inexperto import JugadorInexperto

#
# Configuracion de jugadores para la partida.
# Cuidado de no repetir colores.
#

# La forma que uso para ver si el jugador gano por suerte o por ser
# superior es iniciar una partida, cambiar los roles y jugar con la
# misma semilla. Dejo los jugadores comentados para mas rapidez
jugadores = [
	JugadorSuicida(COLOR_NEGRO, 'Jugador 1'),
	#JugadorInexperto(COLOR_AZUL, 'Jugador 2'),
	#JugadorAprendiz(COLOR_ROJO, 'Jugador 3'),
	JugadorAprendiz(COLOR_AZUL, 'Jugador 2'),
	JugadorInexperto(COLOR_ROJO, 'Jugador 3'),
	JugadorSuicida(COLOR_ROSA, 'Jugador 4'),
]

