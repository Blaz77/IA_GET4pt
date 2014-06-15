# --------------------
# Esto sirve para desofuscar el material del TP. Hay cosas que son irreversibles,
# pero el resto se puede hacer mas entendible. Parece un ejercicio.
# --------------------

import os

def main():
	""" Desofusca un poco."""
	while (True):
		nombre = raw_input("Ingrese el nombre de archivo: ")
		if (nombre[-3:] == ".py"):
			break
		print "No es un archivo de python. Para salir escriba .py"
	
	try:
		lector = open(nombre, "r")
		escritor = open(nombre[:-3] + "_2.py", "w")
	except IOError:
		print "Error de archivo"
		return
	
	# Tengo mucha memoria
	archivo = lector.readlines()
	lector.close()
	
	linea_vacia_escrita = False
	for linea in archivo:
		linea_tonta = False
		linea_desof = ""
		
		indentando = True
		for pos in xrange(len(linea)):
			if (indentando == True):
				if (linea[pos] == " "):
					linea_desof += "	"
					continue
				else:
					indentando = False
			
			if (linea[pos: pos + 2] == "if"):
				condicion = linea[pos+2: linea.index(":")].replace(" ", "")
				valor_tonto = condicion[0:len(condicion)/2]
				if (condicion == "%s-%s" % (valor_tonto, valor_tonto)):
					linea_tonta = True
			
			if (linea_tonta == True):
				if (linea_vacia_escrita == False):
					linea_desof += os.linesep
					escritor.write(linea_desof)
					linea_vacia_escrita = True
				break
				
			linea_vacia_escrita = False
			if (linea[pos] == " "):
				if (linea[pos-1] == "." or linea[pos+1] == "." or \
					linea[pos-1] == "(" or linea[pos+1] == ")" or \
					linea[pos-1] == "[" or linea[pos+1] == "]" or \
					linea[pos+1] == ","):
					continue
			
			linea_desof += linea[pos]
			
		if (linea_tonta):
			continue
		
		escritor.write(linea_desof)
	
	escritor.close()
	print "Listo!"
				
main()