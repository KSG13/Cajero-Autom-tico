#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
#																				#
#	Enrique Sola Gayoso - <kikeelasturianu@gmail.com> - 1/11/2016				#
#	PROYECTO : Cajero automático en Python (BETA) 								#
#																				#
#	Se busca que la terminal a modo de cajero sea lo más dinámica posible		#
#	como si se tratara de un cajero real , con todo lo que conlleva				#
#																				#
#################################################################################
from terminal import *
from terminal_caca import *
import sys
#################################################################################
#Lectura de la contraseña ya que puede varíar a lo largo del curso del programa
password = open("password.txt")
passwordf = password.readline()
password.close()
passwordf = int(passwordf)
#################################################################################
#EMPIEZA CON UN BÚCLE INICIAL PARA LA CONTRASEÑA (NUMEROS OBLIGATORIAMENTE)
# Nº DE INTENTOS (3).
salida = False 
n_attempts = 3
enter = False
print "Introduzca su clave personal , tiene 3 intentos.\n"
while not enter:
	try:
		#Bucle hecho por Javi que encripta la contraseña a posibles mirones
		print ">>>",
		password = ""
		for i in range(0,4):
			car = getch()
			print "*",
			password = password + car 
		password = int(password)
		print
		#password = int(raw_input(">>>"))
		if password == passwordf :
			enter = True
		else:
			n_attempts = n_attempts - 1
			if n_attempts == 0:
				print "Ha excedido el número de intentos , se procederá al bloqueo de la terminal\n"
				time.sleep(3)
				salida = True
	except:
		print "Le recuerdo que su clave está formada por 4 números."
	if salida:
		sys.exit()
#################################################################################
#Bienvenido del usuario y lectura de su saldo. Espera a que el usuario pulse una tecla para continuar con el programa
saldo_archivo = open("saldo.txt")
saldo = saldo_archivo.readline()
saldo_archivo.close()
print ("Bienvenido usuario , su saldo actual es de %s \n.") % (saldo)
print "Pulsa cualquier tecla para continuar"
getch()
#################################################################################
#MENÚ (Usando una versión modificada de mi propia libreria)
caja = True
while caja == True:
	Menu_6opciones("MENÚ" , "" , "(1) - Consultar movimientos" , "(2) - Transferencias y extractos" , "(3) - Ingresos" , "(4) - Saldo actual" , "(5) - Contactos" , "(6) - Ajustes" , "(7) - Salir" )
	print "\n"
#################################################################################
#MENÚ RAÍZ . DE AQUÍ SALE A TODAS LAS OPCIONES DEL MENÚ
	opcion = int(raw_input("A que sección desea acceder?\n"))
#################################################################################
# Esta opción simplemente consultará el archivo "historial.txt" pero a diferencia
# de las otras , no lo modificará , solo lo mostrará en pantalla con los 
# respectivos cambios que haya sufrido por otras opciones
	if opcion == 1 :
		clrscr()
		print "Este es su historial de movimientos en su cuenta:\n"
		historial = open("historial.txt")
		i = 1
		for linea in historial:
			linea = linea.rstrip("\\n")
			print " %4d: %s" % (i, linea)
			i += 1
		historial.close()
		print "Pulsa cualquier tecla para salir"
		getch()
#################################################################################
# Esta opcion opera sobre el documento "historial.txt" y "saldo.txt" .
# En este caso , se trata de transferencias , para envíar una cantidad 
# determinada de dinero a un contacto. 
	if opcion == 2 :
		saldo = float(saldo)
		destinatario = raw_input ("Introduzca el beneficiario de la transacción (MAX: 7 caract.)\n")
		concepto = raw_input ("Introduzca el concepto del movimiento (MAX: 7 caract.)\n")
		cantidad = float(raw_input("Introduzca la cantidad monetaria (MAX: 7 caract.)\n"))
		saldo = saldo - cantidad
		saldo = str(saldo)
		cantidad = str(cantidad)
		fichero = open("saldo.txt" , "w")
		fichero.write(saldo)
		fichero.close()
		fichero = open("historial.txt" , "a")
		linea_destinatario = destinatario + "\t" + "\t" + "\t" + "\t" + "\t"
		fichero.write(linea_destinatario)
		linea_concepto = concepto + "\t" + "\t" + "\t" + "\t" + "\t" + "\t" + "\t" + "\t" 
		fichero.write(linea_concepto)
		linea_cantidad = "-" + cantidad + "\t" +"\n"
		fichero.write(linea_cantidad)
		fichero.close()
		print "OPERACIÓN REALIZADA CON ÉXITO!"
		saldo = float(saldo)
		print "Pulsa cualquier tecla para salir"
		getch()
#################################################################################
# Esta opción la podemos definir como contraria a la anterior. Actua sobre
# los mismos documentos pero en lugar de ser transferencias (restas) son
# ingresos (sumas)
	if opcion == 3 :
		saldo = float(saldo)
		concepto = raw_input ("Introduzca el concepto del movimiento (MAX: 7 caract.)\n")
		cantidad = float(raw_input("Introduzca la cantidad monetaria (MAX: 7 caract.)\n"))
		saldo = saldo + cantidad
		saldo = str(saldo)
		cantidad = str(cantidad)
		fichero = open("saldo.txt" , "w")
		fichero.write(saldo)
		fichero.close()
		fichero = open("historial.txt" , "a")
		linea_destinatario = "------" + "\t" + "\t" + "\t" + "\t" + "\t" + "\t"
		fichero.write(linea_destinatario)
		linea_concepto = concepto + "\t" + "\t" + "\t" + "\t" + "\t" + "\t" + "\t" + "\t" + "\t"
		fichero.write(linea_concepto)
		linea_cantidad = "+" + cantidad + "\t" + "\n"
		fichero.write(linea_cantidad)
		fichero.close()
		print "OPERACIÓN REALIZADA CON ÉXITO!"
		saldo = float(saldo)
		print "Pulsa cualquier tecla para salir"
		getch()
#################################################################################
#OPCIÓN PARA MOSTRAR EL SALDO ACTUAL EN PANTALLA
	if opcion == 4 :
		saldo_archivo = open("saldo.txt")
		saldo = saldo_archivo.readline()
		saldo_archivo.close()
		print ("Su saldo actual es de ") , saldo , ("€")
		print "Pulsa cualquier tecla para salir"
		getch()
#################################################################################
#OPCIÓN PARA MOSTRAR LOS CONTACTOS EN PANTALLA
	if opcion == 5 :
		contactos = open("contactos.txt")
		i = 1
		for linea in contactos:
			linea = linea.rstrip("\\n")
			print " %4d: %s" % (i, linea)
			i += 1
		contactos.close()
		print "Pulsa cualquier tecla para salir"
		getch()
#################################################################################
#Opción para cambiar la contraseña
	if opcion == 6 :
		print "Introduzca la clave de nuevo para confirmación"
		vieja = int(raw_input("Contraseña antigua:"))
		if vieja == passwordf :
			nueva = str(raw_input("Introduzca la nueva contraseña ( 4 dígitos númericos) :\n"))
			password = open("password.txt" , "w")
			password.write(nueva)
			password.close()
			print "Contraseña cambiada con éxito\n"
			print "Pulsa cualquier tecla"
			getch()
		else: 
			print "Contraseña incorrecta, por seguridad , volverá al menú\n"
			print "Pulsa cualquier tecla"
			getch()
#################################################################################
# SALIR
	if opcion == 7 :
		caja = False
#################################################################################	
