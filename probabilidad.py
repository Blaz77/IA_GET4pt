class Probabilidad(object):
    """Coleccion de motores de probabilidades teoricas"""
    def __init__(self):
        self.totales = 0
    def ataque(self, atacante, atacado, minatk = 1, maxdef = 0):
        """Sarasa"""
        #ANDA MAL!!!! No se que le pasa, para ejercitos tipo (2,1) anda, para otros empieza a mandar fruta...
        if atacado <= maxdef: return 0
        elif atacante <= minatk: return 1
        else:
            atacantereal,atacadoreal = min(atacante,4),min(atacado,3)
            for chance in CHANCES[(atacantereal,atacadoreal)]:
                self.totales += CHANCES[(atacantereal,atacadoreal)][chance] * self.ataque(atacante - chance[1], atacado - chance[0], minatk, maxdef)
        total = self.totales
        self.totales = 0
        return total
