#!/usr/bin/python
# -*- coding: utf-8 -*-

fichero = open ( "historial_prueba.txt" , "a" )

historial = True
while historial :
	linea_nueva = raw_input("Introduce la nueva linea para el archivo de texto\n")
	linea_nueva = linea_nueva + "\n"
	if linea_nueva == "0\n" :
		historial = False
	else:
		fichero.write(linea_nueva)

fichero.close()
