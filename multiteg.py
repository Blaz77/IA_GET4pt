from teg import *
from jugador_ejemplo import JugadorOfensivo, JugadorSuicida
from jugador_regular import JugadorRegular
from jugador_aprendiz import JugadorAprendiz
from jugador_inexperto import JugadorInexperto
import random
import time
ganadores = {}
for x in range(100): #range(1403755881,1403755981) son las semillas q uso para testear
        i1I1ii1II1iII = int ( time . time ( ) )
        random . seed ( i1I1ii1II1iII )
        jugadores = [
                JugadorRegular(COLOR_NEGRO, 'Jugador 1'),
                JugadorInexperto(COLOR_AZUL, 'Jugador 2'),
          	#JugadorInexperto(COLOR_ROJO, 'Jugador 3'),
        	#JugadorAprendiz(COLOR_VERDE, 'Jugador 4'),
        	#JugadorOfensivo(COLOR_AMARILLO, 'Jugador 5'),
                #JugadorOfensivo(COLOR_ROSA, 'Jugador 6'),
                ]
        print "Semilla:", i1I1ii1II1iII
        ganador = oo00000o0().jugar( jugadores )
        ganadores[ganador] = ganadores.get(ganador, 0) + 1
        print ganadores
        print
        time.sleep(1)
