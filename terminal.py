#!/usr/bin/python
# coding: utf-8

# -----------------------------------------------------------------------------
# Libreria: terminal.py
# Funciones de atributos del texto y posicionamiento del cursor para 
# terminales ANSI.
# Algunas funciones basadas en conio.h pero con modificaciones
# Javier Salido, 2015 - <javiersago@gmail.com>.
# Última revisión: 28/08/2015 BETA
# -----------------------------------------------------------------------------

import sys, os, tty, time
from select import select

# Atributos del texto
RESETATTR    = 0
BRIGHT       = 1
DIM          = 2
UNDERSCORE   = 4
BLINK        = 5
REVERSE      = 7
HIDDEN       = 8

# Colores para el texto y el fondo
BLACK        = 0
RED          = 1
GREEN        = 2
BROWN        = 3
BLUE         = 4
MAGENTA      = 5
CYAN         = 6
LIGHTGREY    = 7
DARKGREY     = 8
LIGHTRED     = 9
LIGHTGREEN   = 10
YELLOW       = 11
LIGHTBLUE    = 12
LIGHTMAGENTA = 13
LIGHTCYAN    = 14
WHITE        = 15

# Dimensiones de la terminal (SÓLO PARA TERMINALES UNIX)
try:
    TERMHEIGHT, TERMWIDTH = os.popen('stty size', 'r').read().split()
    TERMHEIGHT = int(TERMHEIGHT)
    TERMWIDTH = int(TERMWIDTH)
except:
    TERMHEIGHT, TERMWIDTH = 0, 0

# Borrar completamente la ventana de texto activa y situar el cursor en la
# esquina superior izquierda: posición (1,1)
def clrscr():
    sys.stdout.write('\033[2J\033[1;1H')

# Borrar desde la posición actual del cursor hasta el final de la línea actual.
# La posición del cursor no cambia.
def clreol():
    sys.stdout.write('\033[K')

# Borrar completamente la línea que contenga el cursor. Todas las líneas por
# debajo de esa se mueven para arriba para rellenar el hueco.
def delline():
    sys.stdout.write('\033[2K\033[M')

# Mover el cursor a las coordenadas (x,y) indicadas. Si alguna o ambas
# coordenadas no son válidas, no ocurre nada.
def gotoxy(x,y):
    sys.stdout.write('\033[' + str(y) +';' + str(x) + 'H')

# Ocultar el cursor
def hidecursor():
    sys.stdout.write('\033[?25l')

# Mostrar el cursor
def showcursor():
    sys.stdout.write('\033[?25h')

# Establecer atributos del texto.
def textattr(attr):
    sys.stdout.write('\033[' + str(attr) + 'm')

# Establecer el color con el que se muestran los caracteres en una ventana de
# texto.
def textcolor(color):
    if color < 8:
        color = color + 30
    else:
        color = color + 82
    sys.stdout.write('\033[' + str(color) + 'm')

# Establecer el color de fondo de la pantalla de texto. La llamada a esta 
# función sólo afecta al color de fondo de las escrituras posteriores.    
def textbackground(color):
    if color < 8:
        color = color + 40
    else:
        color = color + 92
    sys.stdout.write('\033[' + str(color) + 'm')

# Establece simultáneamente atributos del texto, color del texto y del fondo.   
def textcba(color, background, attr):
    textattr(attr)
    textcolor(color)
    textbackground(background)
    
# Vacía el contenido del buffer hacia la salida estándar.   
def flush():
    sys.stdout.flush()

# Devuelve el siguiente carácter leído en la consola pero no lo muestra en
# pantalla.
def getch():
	# Inicialización
	file = sys.stdin
	save_attr = tty.tcgetattr(file)
	newattr = save_attr[:]
	newattr[3] &= ~tty.ECHO & ~tty.ICANON
	tty.tcsetattr(file, tty.TCSANOW, newattr)
	
	# getch
	select([file],[],[],0)[0]
	c = file.read(1)
		
	# Restaurar sys.stdin
	tty.tcsetattr(file, tty.TCSADRAIN, save_attr)
	
	return c
	
# Devuelve el siguiente carácter leído en la consola y lo muestra en pantalla.
def getche():
	# Inicialización
	file = sys.stdin
	save_attr = tty.tcgetattr(file)
	newattr = save_attr[:]
	newattr[3] &= tty.ECHO & ~tty.ICANON
	tty.tcsetattr(file, tty.TCSANOW, newattr)
	
	# getche
	select([file],[],[],0)[0]
	c = file.read(1)
	
	# Restaurar sys.stdin
	tty.tcsetattr(file, tty.TCSADRAIN, save_attr)
	
	return c

# Emite un sonido de alerta por la terminal.
def beep():
	sys.stdout.write('\a')
	sys.stdout.flush()

# Dibuja un rectángulo en la ventana de texto a partir de la posición (x,y), de
# ancho w y de alto h.   
def drawbox(x, y, w, h):
    gotoxy(x,y)
    sys.stdout.write('┌')
    for i in range(1,w-1):
        sys.stdout.write('─')
    sys.stdout.write('┐')

    for i in range(1,h-1):
        gotoxy(x,y+i)
        sys.stdout.write('│')
        for j in range(1,w-1):
            sys.stdout.write(' ')
        sys.stdout.write('│')
    gotoxy(x,y+h-1)
    sys.stdout.write('└')
    for i in range(1,w-1):
        sys.stdout.write('─')
    sys.stdout.write('┘')
    
# Borra el contenido de un rectángulo en la ventana de texto a partir de la 
# posición (x,y), de ancho w y de alto h.   
def clearblock(x, y, w, h):
    for i in range(0,h):
        gotoxy(x,y+i)
        for j in range(0,w):
            sys.stdout.write(' ')
    sys.stdout.flush()

# Dibuja la imagen image a partir de la posición (x,y). La imagen es una lista
# de H cadenas de texto de igual longitud W. Esto representa una imagen de WxH
# píxeles. Cada caracter de las cadenas es un dígito hexadecimal (0..F) que
# determina el color del píxel según la tabla de colores.
# Ejemplo: image = [ "000BB000", "000BB000", "00CCCC00", "0C0CC0CB",
#                    "0B0CC000", "00CCCC00", "00C00C00", "00440440" ]
def drawimage(image, x, y):
    # Acomodar image
    image = image[:]            # Clona la imagen
    width = len(image[0])
    if y%2 == 0:                # Coordenada y par; línea impar
        linea1 = "0"*width
        image.insert(0,linea1)
        y = y - 1
    
    height = len(image)
    if height%2 == 1:           # Altura impar
        linea2 = "0"*width
        image.append(linea2)
    height = len(image)

    # Dibujar la imagen
    for i in range(0,height/2):
        gotoxy(x,y)
        linea1 = image[2*i]
        linea2 = image[2*i+1]
        for j in range(0,width):
            alto = linea1[j]
            bajo = linea2[j]
            if alto == '0' and bajo == '0':
                textbackground(0)
                sys.stdout.write(' ')
            elif alto == '0' and bajo !='0':
                textbackground(0)
                textcolor(int(bajo,16))
                sys.stdout.write('▄')
            elif alto != '0' and bajo =='0':
                textbackground(0)
                textcolor(int(alto,16))
                sys.stdout.write('▀')
            elif alto != '0' and bajo !='0' and alto == bajo:
                textcolor(int(alto,16))
                sys.stdout.write('█')
            else:
                textbackground(int(alto,16))
                textcolor(int(bajo,16))
                sys.stdout.write('▄')
        y = y + 1

# -----------------------------------------------------------------------------
