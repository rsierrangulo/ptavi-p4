#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import socket
import sys
""" Cliente que se registra en el servidor """

if len(comandos) != 6:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')
    
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
comandos = sys.argv
linea = comandos[3:6]
expires = linea[2]
# Creamos el contenido que vamos a enviar
if linea[0] == "register":
    LINE = linea[0].upper() + " sip:" + linea[1] + " SIP/2.0" + "\r\n"
    LINE = LINE + "Expires: " + expires + "\r\n\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE)
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
