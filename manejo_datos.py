from os import linesep
import csv
from constantes_probabilidad import *

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

def crear_base(nombre_archivo):
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
                        if linea: diccionario[(desencadenar(linea[0]),desencadenar(linea[1]))] = desencadenar(linea[2])
                return diccionario
        except:
                raise RuntimeError()
        finally:
                archivo.close()

def agregar_proba(nombre_archivo, atacante, atacado, probabilidad):
        try:
                archivo = open(nombre_archivo, "a")
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        linea = ",".join((str(atacante),str(atacado),str(probabilidad)))
        archivo.write(linea+linesep)
        archivo.close()

def crear_base_condicional(nombre_archivo):
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
                        atacante = desencadenar(linea[0])
                        atacado = desencadenar(linea[1])
                        minatk = desencadenar(linea[2])
                        maxdef = desencadenar(linea[3])
                        probabilidad = desencadenar(linea[4])
                        if (atacante, atacado) not in diccionario:
                                diccionario[(atacante, atacado)] = {}
                        diccionario[(atacante,atacado)].update({(minatk,maxdef):probabilidad})
                return diccionario
        except:
                raise RuntimeError()
        finally:
                archivo.close()

def agregar_proba_condicional(nombre_archivo, atacante, atacado, minatk, maxdef, probabilidad):
        try:
                archivo = open(nombre_archivo, "a")
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        linea = ",".join((str(atacante), str(atacado), str(minatk), str(maxdef), str(probabilidad)))
        archivo.write(linea+linesep)
        archivo.close()
