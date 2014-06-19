import csv
from constantes_probabilidad import *

# Campos de las bases de datos
ATACANTE = 0
ATACADO = 1
MINATK = 2
MAXDEF = 3
PROBA_BASICA = 2
PROBA_CONDICIONAL = 4

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

def crear_base(nombre_archivo = "./bases/base.csv"):
        ''' Convierte los datos de nuestro archivo de 
        probabilidades calculadas a un diccionario y 
        lo devuelve.
        '''
        try:
                archivo = open(nombre_archivo, "r")
                archivo_csv = csv.reader(archivo)
        except IOError:
                raise RuntimeError("Error al abrir el archivo de datos")
        try:
                base = {}
                archivo_csv.next()
                for linea in archivo_csv:
                        atacante = desencadenar(linea[ATACANTE])
                        atacado = desencadenar(linea[ATACADO])
                        probabilidad = desencadenar(linea[PROBA_BASICA])
                        if linea: actualizar_base(base, atacante, atacado, probabilidad)
                return base
        except:
                raise RuntimeError("El csv esta todo mal")
        finally:
                archivo.close()

def agregar_proba(nombre_archivo, atacante, atacado, probabilidad, escritura = "a"):
        try:
                archivo = open(nombre_archivo, escritura)
                escritor_csv = csv.writer(archivo)
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        escritor_csv.writerow([atacante, atacado, probabilidad])
        archivo.close()

def actualizar_base(base, atacante, atacado, probabilidad):
        base[(atacante, atacado)] = probabilidad

def crear_base_condicional(nombre_archivo = "./bases/base_condicional.csv"):
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
                base = {}
                archivo_csv.next()
                for linea in archivo_csv:
                        atacante = desencadenar(linea[ATACANTE])
                        atacado = desencadenar(linea[ATACADO])
                        minatk = desencadenar(linea[MINATK])
                        maxdef = desencadenar(linea[MAXDEF])
                        probabilidad = desencadenar(linea[PROBA_CONDICIONAL])
                        if linea: actualizar_base_condicional(base, atacante, atacado, minatk, maxdef, probabilidad)
                return base
        except:
                raise RuntimeError()
        finally:
                archivo.close()

def agregar_proba_condicional(nombre_archivo, atacante, atacado, minatk, maxdef, probabilidad, escritura = "a"):
        try:
                archivo = open(nombre_archivo, escritura)
                escritor_csv = csv.writer(archivo)
        except:
                raise RuntimeError("Error al abrir el archivo: No existe o esta siendo leido por otro")
        escritor_csv.writerow([atacante, atacado, minatk, maxdef, probabilidad])
        archivo.close()

def actualizar_base_condicional(base, atacante, atacado, minatk, maxdef, probabilidad):
        if (atacante, atacado) not in base:
                base[(atacante, atacado)] = {}
        base[(atacante, atacado)].update({(minatk, maxdef): probabilidad})

def _crear_backup(base_backup = CHANCES_GANAR, nombre_archivo = "./bases/base_BACKUP.csv"):
        agregar_proba(nombre_archivo, "Atacante", "Atacado", "Probabilidad", "w")

def _crear_backup_condicional(nombre_archivo = "./bases/base_condicional_BACKUP.csv"):
        agregar_proba_condicional(nombre_archivo, "Atacante", "Atacado", "Minatk", "Maxdef", "Probabilidad", "w")

def _flushear_archivo():
        _crear_backup(nombre_archivo = "./bases/base.csv")

def _flushear_archivo_condicional():
        _crear_backup_condicional("./bases/base_condicional.csv")
