#from random import randrange,randint
class Simulador(object):
    """Motores de simulacion de probabilidades para situaciones aleatorias"""
    def __init__(self, probabilidad = 0):
        self.probabilidad = probabilidad
        
    def ataque_individual(self, dado, atacante, atacado, minatk = 1, maxdef = 0):
        """ Recibe un dado, la cantidad de ejercitos de cada 
        lado, un minimo de ejercitos a conservar, y un minimo 
        de ejercitos enemigos a destruir. Devuelve True si 
        consigue destruir el minimo de ejercitos enemigos 
        o False si no lo logra para cuando  le quedan igual 
        o menos ejercitos que el minimo.
        """
        if atacado <= maxdef:
	        return True
        elif atacante <= minatk:
	        return False
        else:
	        dado.lanzar_dados(atacante,atacado)
	        return ganaste_combate_aleatorio(atacante - dado.ejercitos_perdidos_atacante(),atacado - dado.ejercitos_perdidos_atacado(), minatk, maxdef)

    def chances_ataque(self, dado, atacante, atacado, minatk = 1, maxdef = 0):
        """ Corre mil veces la funcion ataque_individual, y 
        devuelve la probabilidad (estimada) de victoria con 
        esos ejercitos y limites"""
            total = 1000
            ganados = 0
            for i in range(1000):
            	gane_combate = ganaste_combate_aleatorio(atacante, atacado, minatk, maxdef)
            	if gane_combate:
            	    ganados += 1
            return ganados*1.0/1000

        
        
