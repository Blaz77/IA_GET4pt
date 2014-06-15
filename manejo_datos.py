from os import linesep
import csv

def desencadenar(valor):
        ''' Recibe una cadena numerica y la convierte a
        int o float, segun si es un numero entero o no,
        respectivamente.
        '''
        try:
                valor = float(valor)
                if valor == int(valor):
                        valor = int(valor)
                return valor
        except:
                raise ValueError("Recibio un valor no numerico!")

def csv_a_diccionario(nombre_archivo):
        ''' Convierte los datos de nuestro archivo de 
        probabilidades calculadas a un diccionario y 
        lo devuelve.
        '''
        try:
                archivo = open(nombre_archivo)
                archivo_csv = csv.reader(archivo)
        except IOError:
                raise RuntimeError("Error al abrir el archivo de datos")
        try:
                diccionario = {}
                archivo_csv.next()
                for linea in archivo_csv:
                        diccionario[(desencadenar(linea[0]),desencadenar(linea[1]))] = desencadenar(linea[2])
                return diccionario
        except:
                raise RuntimeError()
        finally:
                archivo.close()

def agregar_probabilidad(archivo, atacante, atacado, probabilidad):
        try:
                abierto = open(archivo, "a")
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        linea = ",".join(str(atacante),str(atacado),str(probabilidad))
        abierto.write(linea+linesep)
        abierto.close()
